import os
import arxiv
from pathlib import Path

if __name__ == '__main__':
    curr_dir = Path(__file__).resovle().parent

    if not os.path.exists(str(curr_dir / 'Papers')):
        os.makedirs(str(curr_dir / 'Papers'))