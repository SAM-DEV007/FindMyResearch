import torch

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("clip-ViT-B-32")

import fitz
from tqdm import tqdm

import io

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import pickle as pkl


def load_pdf():
    global embedder

    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

    changes = False

    corpus = load_file('semantic_sentence.dat')
    if not corpus:
        corpus = {}

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
        save_file(corpus, 'semantic_sentence.dat')


def load_images():
    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

    main_images = load_file('semantic_image.dat')
    if not main_images:
        main_images = {}

    changes = False

    for pdf in tqdm(os.listdir(paper_dir)):
        if pdf in main_images:
            continue

        doc = fitz.open(f'{paper_dir}/{pdf}')
        image_list = []

        for page in doc:
            image_list.extend(page.get_images())

        if not image_list:
            continue
        
        changes = True

        images = preprocess_images(image_list, doc)

        embeddings = get_image_embeddings(images)
        main_images[pdf] = embeddings
    
    if changes:
        save_file(main_images, 'semantic_image.dat')


def preprocess_images(image_list, doc):
    images = []

    for img in image_list:
        xref = img[0]

        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        if image.size[0] <= 1 or image.size[1] <= 1:
            continue

        images.append(image)

    return images


def get_image_embeddings(image_tensors):
    embeddings = model.encode(image_tensors, convert_to_tensor=True)

    return embeddings


def semantic_search(corpus: dict, query: str, num_search: int = 10):
    global embedder

    corpus_embeddings = list(corpus.values())
    keys = list(corpus.keys())

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=num_search)
    hits = hits[0]

    pdfs = {keys[hit['corpus_id']]: float(f'{hit["score"]:.4f}') for hit in hits}
    
    return pdfs


def image_semantic_search(main_images: dict, query: str, num_search: int = 10):
    global model

    query_embedding = model.encode([query], convert_to_tensor=True)

    hits = {}
    for pdf_name, image_data in main_images.items():
        for image in image_data:
            score = util.cos_sim(image, query_embedding).squeeze().tolist()
            if not hits.get(pdf_name) and len(hits) < num_search:
                hits[pdf_name] = score
                continue

            if hits.get(pdf_name) and score > hits[pdf_name]:
                hits[pdf_name] = score 

            if score > min(hits.values()):
                min_key = min(hits, key=hits.get)
                hits.pop(min_key)

                hits[pdf_name] = score  

    return hits


def save_file(_dict: dict, name: str):
    cache_location = str(Path(__file__).resolve().parent.parent / '.cache/semantic_rp')

    if not os.path.exists(cache_location):
        os.makedirs(cache_location)
    
    with open(f'{cache_location}/{name}', 'wb') as f:
        pkl.dump(_dict, f, protocol=pkl.HIGHEST_PROTOCOL)


def load_file(name: str):
    cache_location = str(Path(__file__).resolve().parent.parent / '.cache/semantic_rp')

    if not os.path.exists(f'{cache_location}/{name}'):
        return False

    with open(f'{cache_location}/{name}', 'rb') as f:
        _dict = pkl.load(f)
    
    return _dict