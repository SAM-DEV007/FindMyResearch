from pypdf import PdfReader
import re
from pathlib import Path
import os
import random

paper_dir = Path(__file__).resolve().parent.parent / 'Papers'
pdf = random.choice(os.listdir(paper_dir))

reader = PdfReader(f'{paper_dir}/{pdf}')
metadata = reader.metadata

print(metadata.author, metadata.title, metadata.creation_date, sep='\n')

from datetime import datetime
print(metadata.creation_date.strftime('%d-%m-%Y'))