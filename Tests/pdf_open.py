import webbrowser
from pathlib import Path
import os

paper_dir = Path(__file__).resolve().parent / 'TestPapers'
paper = os.listdir(paper_dir)[0]

webbrowser.open(f'{paper_dir}/{paper}', new=2)