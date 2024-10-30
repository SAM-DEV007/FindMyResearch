import os

from arxiv import Client, Search, SortCriterion
from pathlib import Path
from tqdm import tqdm

if __name__ == '__main__':
    curr_dir = Path(__file__).resolve().parent
    total_papers = 800

    if not os.path.exists(str(curr_dir / 'Papers')):
        os.makedirs(str(curr_dir / 'Papers'))

    client = Client(
        page_size=total_papers
    )
    search = Search(
        query='all', 
        max_results=total_papers, 
        sort_by = SortCriterion.SubmittedDate
    )

    for paper in tqdm(client.results(search), total=total_papers):
        paper.download_pdf(dirpath=str(curr_dir / 'Papers'))