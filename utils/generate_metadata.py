import pdf2doi
pdf2doi.config.set('verbose', False)

import fitz
import re
import json

from pathlib import Path
import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from transformers import pipeline
model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

from datetime import datetime
from pypdf import PdfReader
from tqdm import tqdm

from datetime import datetime


def generate_metadata_main():
    metadata = {}

    metadata, force = generate_metadata_doi(metadata)
    if force:
        metadata = generate_metadata_manual(metadata)
    
    save_metadata(metadata)


def generate_metadata_doi(metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    results = pdf2doi.pdf2doi(paper_dir)

    force = False

    for i in tqdm(range(len(results))):
        pdf = results[i]['path'].split('\\')[-1]
        data = json.loads(results[i]['validation_info'])

        if pdf in metadata:
            continue

        if not data:
            force = True
            continue

        metadata[pdf] = {}

        metadata[pdf]['title'] = data['title']
        metadata[pdf]['author'] = get_author(data['author'])
        metadata[pdf]['keywords'] = ','.join(data['categories'])
        metadata[pdf]['date'] = str(data['issued']['date-parts'][0][0])
        metadata[pdf]['publisher'] = data['publisher']
        metadata[pdf]['abstract'] = data['abstract']
        metadata[pdf]['doi'] = data['DOI']
    
    return metadata, force


def generate_metadata_manual(metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')

    for pdf in tqdm(os.listdir(paper_dir)):
        if pdf in metadata:
            continue

        doc = fitz.open(f'{paper_dir}/{pdf}')
        page = doc[0]
        blocks = page.get_text("blocks")

        text_list = [block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', ' ') for block in blocks]

        idx = get_idx(text_list)

        title = text_list[idx]
        author = text_list[idx+1]

        keyword, date = generate_metadata_ai(text_list)
        _title, _author, _date = generate_metadata_pdf(paper_dir, pdf)

        if not title and _title:
            title = _title
        if not author and _author:
            author = _author
        if (not date or len(date) == 4) and _date:
            date = _date
        
        metadata[pdf] = {}
            
        metadata[pdf]['title'] = title
        metadata[pdf]['author'] = author
        metadata[pdf]['date'] = date

        metadata[pdf]['keywords'] = keyword

        metadata[pdf]['publisher'] = ''
        metadata[pdf]['abstract'] = ''
        metadata[pdf]['doi'] = ''
    
    return metadata


def generate_metadata_ai(text_list):
    global question_answerer

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
    
    try:
        date['answer'] = datetime.strptime(date['answer'], "%d %b %Y").strftime('%d-%m-%Y')
    except ValueError:
        date['answer'] = date['answer'][-4:]

    return keyword['answer'], date['answer']


def generate_metadata_pdf(paper_dir: str, pdf: str):
    reader = PdfReader(f'{paper_dir}/{pdf}')
    metadata = reader.metadata
    date = metadata.creation_date

    if isinstance(date, datetime):
        date = metadata.creation_date.strftime('%d-%m-%Y')

    return metadata.title, metadata.author, date


def get_author(data: list):
    return ','.join([i['given'] + ' ' + i['family'] for i in data])


def get_idx(text_list):
    return int(bool(re.search(r'\d', text_list[0])))


def save_metadata(metadata: dict):
    cache_dir = str(Path(__file__).resolve().parent.parent / '.cache/metadata_rp')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(f'{cache_dir}/metadata.json', 'w') as f:
        json.dump(metadata, f)


def load_metadata():
    cache_dir = str(Path(__file__).resolve().parent.parent / '.cache/metadata_rp')

    with open(f'{cache_dir}/metadata.json', 'r') as f:
        metadata = json.load(f)
    
    return metadata