import torch

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")

import fitz
from tqdm import tqdm

paper_dir = Path(__file__).resolve().parent.parent / 'Papers'
num_search = 3
max_score = {}

query = [
    "A man is eating pasta.",
]

query_embedding = embedder.encode(query, convert_to_tensor=True)

for pdf in tqdm(os.listdir(paper_dir)):
    corpus = []

    doc = fitz.open(f'{paper_dir}/{pdf}')
    text_list = []
    for page in doc:
        blocks = page.get_text("blocks")

        text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

    context = '. '.join(text_list)
    corpus.append(context)

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=1)
    hit = hits[0][0]

    # print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    if len(max_score) < num_search:
        max_score[hit['score']] = pdf
    else:
        if hit['score'] > min(max_score.keys()):
            max_score.pop(min(max_score.keys()))
            max_score[hit['score']] = pdf
        
print(max_score)
        