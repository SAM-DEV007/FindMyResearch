import os
import logging

from urllib.request import urlcleanup
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from tqdm import tqdm

def cleanup():
    urlcleanup()

def verify_files(download_path: str):
    logger = logging.getLogger("pypdf")
    logger.setLevel(logging.ERROR)

    data = {
        'correct': 0,
        'error': 0
    }

    print('Verifying downloaded files')
    for file in tqdm(os.listdir(download_path)):
        try:
            with open(download_path + '/' + file, 'rb') as f:
                PdfReader(f)
            data['correct'] += 1
        except PdfReadError:
            os.remove(download_path + '/' + file)
            print(f'\nError reading {file} as pdf. Removed.')
            data['error'] += 1
    print(f'Correct files: {data["correct"]}\nError files: {data["error"]}\nTotal files: {data["correct"] + data["error"]}')
    print('Verification complete')