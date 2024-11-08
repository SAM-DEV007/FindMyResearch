import re
import fitz
from pathlib import Path
import os

import metadata_main
import json

from tqdm import tqdm


def pdf_search(search: str, context: str):
    return bool(re.search(search, context, flags=re.IGNORECASE))


def metadata_search(keyword: str, sub_metadata: dict, search_type: str):
    return bool(re.search(keyword, sub_metadata[search_type], flags=re.IGNORECASE))


def generate_context():
    main_context = load_context()
    if not main_context:
        main_context = {}
    
    changes = False

    paper_dir = Path(__file__).resolve().parent / 'TestPapers'
    for pdf in tqdm(os.listdir(paper_dir)):
        if pdf in main_context:
            continue
            
        changes = True

        doc = fitz.open(f'{paper_dir}/{pdf}')
        text_list = []
        for page in doc:
            blocks = page.get_text("blocks")

            text_list.extend([block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks])

        context = '. '.join(text_list)
        main_context[pdf] = context
    
    if changes:
        save_context(main_context)


def save_context(main_context):
    cache_dir = Path(__file__).resolve().parent / 'TestFiles/metadata_rp'

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(f'{cache_dir}/context.json', 'w') as f:
        json.dump(main_context, f)


def load_context():
    cache_dir = Path(__file__).resolve().parent / 'TestFiles/metadata_rp'

    if not os.path.exists(f'{cache_dir}/context.json'):
        return False

    with open(f'{cache_dir}/context.json', 'r') as f:
        main_context = json.load(f)
    
    return main_context


def text_search(context: dict):
    return [pdf for pdf, content in context.items() if pdf_search(word, content)]


def metadata_search_all(metadata: dict, word: str):
    return [pdf for pdf, sub_metadata in metadata.items() if any(metadata_search(word, sub_metadata, main_word) for main_word in ('title', 'author', 'keywords', 'date', 'publisher', 'abstract', 'doi'))]
            


metadata_main.generate_metadata_main()
metadata = metadata_main.load_metadata()

generate_context()
context = load_context()

word = 'result'

print(text_search(context))
print(metadata_search_all(metadata, word))