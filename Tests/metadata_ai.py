from pathlib import Path

import os
os.environ['HF_HOME'] = str(Path(__file__).parent.parent / '.cache')

from transformers import pipeline

#model_checkpoint = "huggingface-course/bert-finetuned-squad"
model_checkpoint = "deepset/roberta-base-squad2"
question_answerer = pipeline("question-answering", model=model_checkpoint)

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

text_list = [block[4].encode('ascii', 'ignore').strip().decode('utf-8').replace('\n', '') for block in blocks]

context = '. '.join(text_list)

print(context)

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

print()
print(keyword['answer'], date['answer'], sep='\n')

from datetime import datetime
print(datetime.strptime(date['answer'], "%d %b %Y").strftime('%d-%m-%Y'))
    