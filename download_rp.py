import os

from arxiv import Client, Search, SortCriterion, SortOrder
from pathlib import Path
from tqdm import tqdm
from utils.download_paper import cleanup, verify_files

if __name__ == '__main__':
    curr_dir = Path(__file__).resolve().parent
    download_dir = str(curr_dir / 'Papers')
    total_papers = 500

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    client = Client(
        page_size=total_papers
    )
    search = Search(
        query='all', 
        max_results=total_papers, 
        sort_by = SortCriterion.SubmittedDate,
        sort_order = SortOrder.Descending
    )

    for paper in tqdm(client.results(search), total=total_papers):
        paper.download_pdf(dirpath=download_dir)

    cleanup()
    verify_files(download_dir)