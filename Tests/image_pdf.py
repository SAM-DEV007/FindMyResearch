from pathlib import Path
import fitz 
import io
from PIL import Image
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

import torch
from torchvision import transforms
from sentence_transformers import SentenceTransformer, util

from tqdm import tqdm

model = SentenceTransformer("clip-ViT-B-32")


def preprocess_images(image_list):
    images = []

    for img in image_list:
        xref = img[0]

        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        '''
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        '''
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        #image = transform(image)

        images.append(image)

    return images


def get_image_embeddings(image_tensors):
    embeddings = model.encode(image_tensors, convert_to_tensor=True)

    return embeddings


def get_text_embeddings(text):
    embeddings = model.encode([text], convert_to_tensor=True)

    return embeddings


paper_dir = Path(__file__).resolve().parent / 'TestPapers'

main_images = {}
for pdf in tqdm(os.listdir(paper_dir)):
    doc = fitz.open(f'{paper_dir}/{pdf}')
    image_list = []

    for page in doc:
        image_list.extend(page.get_images())
    images = preprocess_images(image_list)

    embeddings = get_image_embeddings(images)
    main_images[pdf] = embeddings

query = 'machine learning'
query_embedding = get_text_embeddings(query)

num_search = 10
hits = {}
for pdf_name, image_data in main_images.items():
    for image in image_data:
        # print(f'{util.cos_sim(image, query_embedding).squeeze().tolist():.4f}')
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

print(hits) 