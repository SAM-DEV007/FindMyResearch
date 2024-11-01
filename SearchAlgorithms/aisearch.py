import torch

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")

import fitz


def semantic_search(query: str, num_search: int):
    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'
    max_score = {}

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    corpus = {}
    for pdf in tqdm(os.listdir(paper_dir)):
        doc = fitz.open(f'{paper_dir}/{pdf}')
        text_list = []
        for page in doc:
            blocks = page.get_text("blocks")

            text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

        context = '. '.join(text_list)
        corpus[pdf] = context

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=min(num_search, len(corpus)))
    hits = hits[0][0]

    for hit in hits:
        if len(max_score) < num_search:
            max_score[hit['score']] = pdf
        else:
            if hit['score'] > min(max_score.keys()):
                max_score.pop(min(max_score.keys()))
                max_score[hit['score']] = pdf

    return max_score