import pdf2doi
pdf2doi.config.set('verbose', False)

import fitz
import re
import json

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from transformers import pipeline
from datetime import datetime
from pypdf import PdfReader


def generate_metadata_main():
    pass


def generate_metadata_doi():
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')

    metadata = {}
    results = pdf2doi.pdf2doi(paper_dir)

    for i in len(results):
        data = json.loads(results[i]['validation_info'])

        metadata[data['title']]['title'] = data['title']
        metadata[data['title']]['author'] = get_author(data['author'])
        metadata[data['title']]['keywords'] = ','.join(data['categories'])
        metadata[data['title']]['date'] = data['issues']['date-parts'][0][0]
        metadata[data['title']]['publisher'] = data['publisher']
        metadata[data['title']]['abstract'] = data['abstract']
        metadata[data['title']]['doi'] = data['DOI']
    
    return metadata


def generate_metadata_manual():
    pass


def generate_metadata_ai():
    pass


def generate_metadata_pdf():
    pass


def get_author(data: list):
    return ','.join([i['given'] + ' ' + i['family'] for i in data])


def save_metadata():
    cache_dir = str(Path(__file__).resolve().parent.parent / '.cache/metadata_rp')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(f'{cache_dir}/metadata.json', 'wb') as f:
        json.dump(metadata, f)


def load_metadata():
    cache_dir = str(Path(__file__).resolve().parent.parent / '.cache/metadata_rp')

    with open(f'{cache_dir}/metadata.json', 'rb') as f:
        metadata = json.load(f)
    
    return metadata