import torch

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")

import fitz


def load_pdf():
    global embedder

    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

    corpus = {}
    for pdf in os.listdir(paper_dir):
        doc = fitz.open(f'{paper_dir}/{pdf}')
        text_list = []
        for page in doc:
            blocks = page.get_text("blocks")

            text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

        context = '. '.join(text_list)
        corpus[pdf] = context

    corpus_embeddings = embedder.encode(list(corpus.values()), convert_to_tensor=True)
    keys = list(corpus.keys())
    return corpus_embeddings, keys


def semantic_search(corpus_embeddings, keys: list, query: str, num_search: int = 10):
    global embedder

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=num_search)
    hits = hits[0]

    pdfs = {keys[hit['corpus_id']]: float(f'{hit["score"]:.4f}') for hit in hits}
    
    return pdfs