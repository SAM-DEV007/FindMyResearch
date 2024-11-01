import torch

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")

import fitz
import pickle as pkl


def load_pdf():
    global embedder

    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

    corpus = load_file()
    if not corpus:
        corpus = {}
    
    changes = False

    for pdf in tqdm(os.listdir(paper_dir)):
        if pdf in corpus:
            continue
            
        changes = True

        doc = fitz.open(f'{paper_dir}/{pdf}')
        text_list = []
        for page in doc:
            blocks = page.get_text("blocks")

            text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

        context = '. '.join(text_list)
        corpus[pdf] = embedder.encode(context, convert_to_tensor=True)
    
    if changes:
        save_file(corpus)


def semantic_search(corpus: dict, query: str, num_search: int = 10):
    global embedder

    corpus_embeddings = list(corpus.values())
    keys = list(corpus.keys())

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=num_search)
    hits = hits[0]

    pdfs = {keys[hit['corpus_id']]: float(f'{hit["score"]:.4f}') for hit in hits}
    
    return pdfs


def save_file(corpus: dict):
    cache_location = str(Path(__file__).resolve().parent.parent / '.cache/semantic_rp')

    if not os.path.exists(cache_location):
        os.makedirs(cache_location)
    
    with open(f'{cache_location}/semantic.dat', 'wb') as f:
        pkl.dump(corpus, f, protocol=pkl.HIGHEST_PROTOCOL)


def load_file():
    cache_location = str(Path(__file__).resolve().parent.parent / '.cache/semantic_rp')

    if not os.path.exists(f'{cache_location}/semantic.dat'):
        return False

    with open(f'{cache_location}/semantic.dat', 'rb') as f:
        corpus = pkl.load(f)
    
    return corpus