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

metadata = {}

paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')


def generate_metadata_main():
    pass


def generate_metadata_doi():
    results = pdf2doi.pdf2doi(paper_dir)

    for i in len(results):
        data = json.loads(results[i]['validation_info'])

        metadata[data['DOI']]['title'] = data['title']
        metadata[data['DOI']]['author'] = get_author(data['author'])
        metadata[data['DOI']]['keywords'] = ','.join(data['categories'])
        metadata[data['DOI']]['date'] = data['issues']['date-parts'][0][0]
        metadata[data['DOI']]['publisher'] = data['publisher']
        metadata[data['DOI']]['abstract'] = data['abstract']


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