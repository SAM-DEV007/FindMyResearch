import torch

from pathlib import Path
import os
import random
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")
'''
import fitz
from tqdm import tqdm

paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

corpus = []

for pdf in tqdm(os.listdir(paper_dir)):
    doc = fitz.open(f'{paper_dir}/{pdf}')
    text_list = []
    for page in doc:
        blocks = page.get_text("blocks")

        text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

    context = '. '.join(text_list)
    corpus.append(context)
'''
text = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
]

corpus = {
    random.randint(1, 100):text[i] for i in range(len(text))
}

corpus_embeddings = embedder.encode(list(corpus.values()), convert_to_tensor=True)

query = [
    "A man is eating pasta.",
]

query_embedding = embedder.encode(query, convert_to_tensor=True)

hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=min(3, len(corpus)))
print(hits)
hits = hits[0]
keys = list(corpus.keys())
print(corpus)
for hit in hits:
    print(list(corpus.values())[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    print(keys[hit['corpus_id']])