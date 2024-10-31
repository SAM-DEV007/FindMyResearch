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

from datetime import datetime


def generate_metadata_main():
    pass


def generate_metadata_doi(metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    results = pdf2doi.pdf2doi(paper_dir)

    for i in len(results):
        data = json.loads(results[i]['validation_info'])

        if not data or not data['title']:
            continue

        metadata[data['title']]['title'] = data['title']
        metadata[data['title']]['author'] = get_author(data['author'])
        metadata[data['title']]['keywords'] = ','.join(data['categories'])
        metadata[data['title']]['date'] = data['issues']['date-parts'][0][0]
        metadata[data['title']]['publisher'] = data['publisher']
        metadata[data['title']]['abstract'] = data['abstract']
        metadata[data['title']]['doi'] = data['DOI']
    
    return metadata


def generate_metadata_manual(metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')

    for pdf in os.listdir(paper_dir):
        doc = fitz.open(f'{paper_dir}/{pdf}')
        page = doc[0]
        blocks = page.get_text("blocks")

        text_list = [block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', ' ') for block in blocks]

        idx = get_idx(text_list)

        title = text_list[idx]
        author = text_list[idx+1]

        if not metadata[title]:
            continue

        metadata[title]['title'] = title
        metadata[title]['author'] = author
    
    return metadata


def generate_metadata_ai(metadata, text_list):
    model_checkpoint = "deepset/roberta-base-squad2"
    question_answerer = pipeline("question-answering", model=model_checkpoint)

    context = '. '.join(text_list)

    question = "What are the keywords?"
    keyword = question_answerer(question=question, context=context, handle_impossible_answer=True)

    question = "What is the date?"
    date = question_answerer(question=question, context=context, handle_impossible_answer=False)

    for s in context[keyword['end']:]:
        if s == '.':
            break
        keyword['answer'] += s
    if keyword['start'] in range(50):
        keyword['answer'] = ''
    
    date['answer'] = datetime.strptime(date['answer'], "%d %b %Y").strftime('%d-%m-%Y')

    return keyword['answer'], date['answer']


def generate_metadata_pdf():
    pass


def get_author(data: list):
    return ','.join([i['given'] + ' ' + i['family'] for i in data])


def get_idx(text_list):
    return int(bool(re.search(r'\d', text_list[0])))


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