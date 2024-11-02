import fitz
from pathlib import Path
import os
import re
import random

paper_dir = Path(__file__).resolve().parent.parent / 'Papers'
pdf = random.choice(os.listdir(paper_dir))

doc = fitz.open(f'{paper_dir}/{pdf}')
page = doc[0]
blocks = page.get_text("blocks")

text_list = [block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', ' ') for block in blocks]

def get_idx(text_list):
    return int(bool(re.search(r'\d', text_list[0])))

idx = get_idx(text_list)

title = text_list[idx]
author = text_list[idx+1]

print(title, author, sep='\n')