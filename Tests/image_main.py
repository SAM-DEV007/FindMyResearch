from pathlib import Path
import fitz 
import io

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

import torch
from sentence_transformers import SentenceTransformer, util

from tqdm import tqdm

model = SentenceTransformer("clip-ViT-B-32")


def load_images():
    paper_dir = Path(__file__).resolve().parent.parent / 'Papers'

    main_images = {}
    for pdf in tqdm(os.listdir(paper_dir)):
        doc = fitz.open(f'{paper_dir}/{pdf}')
        image_list = []

        for page in doc:
            image_list.extend(page.get_images())
        images = preprocess_images(image_list, doc)

        embeddings = get_image_embeddings(images)
        main_images[pdf] = embeddings
    
    return main_images


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


query = 'machine learning'

main_images = load_images()
hits = image_semantic_search(main_images, query)

print(hits)