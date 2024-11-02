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


def check_metadata():
    force = False
    main_force = False

    cache_dir = str(Path(__file__).resolve().parent.parent / '.cache/metadata_rp')
    if not os.path.exists(f'{cache_dir}/metadata.json'):
        return False, force

    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    metadata = load_metadata()

    delete_metadata = []
    for pdf in metadata:
        if not os.path.exists(f'{paper_dir}/{pdf}'):
            delete_metadata.append(pdf)
    for pdf in delete_metadata:
        metadata.pop(pdf)
        
    for pdf in os.listdir(paper_dir):
        if pdf not in metadata:
            metadata, force = generate_metadata_individual(metadata, pdf)
            if force:
                main_force = True
    
    return metadata, main_force


def generate(metadata: dict, pdf: str, data: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    force = False

    metadata[pdf] = {}

    try:
        metadata[pdf]['title'] = data['title']
        metadata[pdf]['author'] = get_author(data['author'])
        metadata[pdf]['publisher'] = data['publisher']

        _, _, date = generate_metadata_pdf(paper_dir, pdf)
        if not date:
            date = str(data['issued']['date-parts'][0][0])
        metadata[pdf]['date'] = date

        keywords = ''
        doi = ''
        abstract = ''

        if 'DOI' not in data or 'categories' not in data or 'abstract' not in data:
            doc = fitz.open(f'{paper_dir}/{pdf}')
            page = doc[0]
            blocks = page.get_text("blocks")

            text_list = [block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', ' ') for block in blocks]

            keywords, _, doi = generate_metadata_ai(text_list)
            keyword, abstract = generate_keyabs(text_list, keywords)

        if 'DOI' in data:
            doi = data['DOI']
        metadata[pdf]['doi'] = doi

        if 'categories' in data:
            keywords = ','.join(data['categories'])
        metadata[pdf]['keywords'] = keywords

        if 'abstract' in data:
            abstract = data['abstract']
        metadata[pdf]['abstract'] = abstract
    except:
        del metadata[pdf]
        force = True
    
    return metadata, force


def generate_keyabs(text_list: list, keyword: str):
    _abstract = ''
    found_abstract = False

    for txt in text_list:
        if found_abstract:
            _abstract = txt
            break
        if bool(re.search('abstract', txt, flags=re.IGNORECASE)):
            if len(txt) <= len('abstract') + 10:
                found_abstract = True
                continue
            _abstract = txt
            break
    if _abstract:
        if 'introduction' in _abstract.lower():
            _abstract = _abstract.split('introduction')[0]
    
    if not keyword:
        found_keyword = False
        for txt in text_list:
            if found_keyword:
                keyword = txt
                break
            if bool(re.search('key.?word', txt, flags=re.IGNORECASE)):
                if len(txt) <= len('keyword') + 10:
                    found_keyword = True
                    continue
                keyword = txt
                break
    
    return keyword, _abstract


def generate_metadata_individual(metadata: dict, pdf: str):
    force = False

    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    results = pdf2doi.pdf2doi(f'{paper_dir}/{pdf}')

    try:
        data = json.loads(results['validation_info'])
    except:
        data = None

    if not data:
        force = True
        return metadata, force

    metadata, force = generate(metadata, pdf, data)

    return metadata, force


def generate_metadata_main():
    print('Main technique for metadata generation')
    metadata, force = check_metadata()
    if not metadata:
        print('Checks failed, regenerating metadata')
        metadata = {}
        metadata, force = generate_metadata_doi(metadata)
    if force:
        print('Backup technique for metadata generation')
        metadata = generate_metadata_manual(metadata)
    print('Metadata generation complete')
    
    save_metadata(metadata)


def generate_metadata_doi(metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent.parent / 'Papers')
    results = pdf2doi.pdf2doi(paper_dir)

    force = False

    for i in tqdm(range(len(results))):
        pdf = results[i]['path'].split('\\')[-1]

        try:
            data = json.loads(results[i]['validation_info'])
        except:
            data = None

        if pdf in metadata:
            continue

        if not data:
            force = True
            continue

        metadata, force = generate(metadata, pdf, data)
    
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

        keyword, date, doi = generate_metadata_ai(text_list)
        _title, _author, _date = generate_metadata_pdf(paper_dir, pdf)

        keyword, _abstract = generate_keyabs(text_list, keyword)

        if not title and _title:
            title = _title
        if not author and _author:
            author = _author
        if (not date or len(date) == 4) and _date:
            date = _date
        
        if not title and not _title:
            title = keyword
        
        metadata[pdf] = {}
            
        metadata[pdf]['title'] = title
        metadata[pdf]['author'] = author
        metadata[pdf]['date'] = date

        metadata[pdf]['keywords'] = keyword

        metadata[pdf]['publisher'] = ''
        metadata[pdf]['abstract'] = _abstract
        metadata[pdf]['doi'] = doi
    
    return metadata


def generate_metadata_ai(text_list):
    global question_answerer

    context = '. '.join(text_list)

    question = "What are the keywords?"
    keyword = question_answerer(question=question, context=context, handle_impossible_answer=True)

    question = "What is the date?"
    date = question_answerer(question=question, context=context, handle_impossible_answer=False)

    question = "What is the doi?"
    doi = question_answerer(question=question, context=context, handle_impossible_answer=True)

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

    return keyword['answer'], date['answer'], doi['answer']


def generate_metadata_pdf(paper_dir: str, pdf: str):
    reader = PdfReader(f'{paper_dir}/{pdf}')
    metadata = reader.metadata
    date = metadata.creation_date

    if metadata.author:
        if metadata.author.isnumeric():
            metadata.author = ''

    if isinstance(date, datetime):
        date = metadata.creation_date.strftime('%d-%m-%Y')

    return metadata.title, metadata.author, date


def get_author(data: list):
    return ','.join([i['given'] + ' ' + i['family'] for i in data])


def get_idx(text_list):
    return bool(re.search(r'\d\d\d\d', text_list[0]))


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