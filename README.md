# FindMyResearch
Find and filter research papers.

A Streamlit application to search, sort and filter research papers.\
Search for a paper using word, phrase, sentence or a question.

**Search algorithms**:

The search algorithms are robust and can be used with any research paper. More [information](#working) on how it works.
- Semantic (Text): Semantic search to find the most possible match among the corpus of the papers.
- Semantic (Image): Semantic search to find the most possible match among the images of the papers.
- Text: Word, Phrase or Sentence match among the corpus of the papers.
- Metadata: Word, Phrase or Sentence match among the metadata of the papers.
- File Name: File name match among the saved papers.

**Sort**:

More [information](#working) on how it works.
- **Sort Field**
   - Relevance: (Only available in Semantic search) Sort on the basis of relevance with the search.
   - Title: Sort on the basis of title.
   - Author: Sort on the basis of author.
   - Keywords: Sort on the basis of keywords.
   - Date: Sort on the basis of date.
   - Publisher: Sort on the basis of publisher.
   - Abstract: Sort on the basis of abstract.
   - Doi: Sort on the basis of DOI.
- **Sort Order**
   - Decrease: Sort in descending order.
   - Increase: Sort in ascending order.

**Filter**:

More [information](#working) on how it works.
- **Max. Number of Results**: The maximum number of results to be considered.
- **Filter Field** (Used with Filter, if the Filter is empty, it is ignored)
  - Title: Filter on the basis of title.
  - Author: Filter on the basis of author.
  - Keywords: Filter on the basis of keywords.
  - Date: Filter on the basis of date.
  - Publisher: Filter on the basis of publisher.
  - Abstract: Filter on the basis of abstract.
  - Doi: Filter on the basis of DOI.
- **Filter**: (Used with Filter Field) Filter on the basis of the text.

## Installation
### Python version
Python 3.x or greater is required.

### Clone the repository
```bash
git clone https://github.com/SAM-DEV007/FindMyResearch.git
cd FindMyResearch
```

### Create a virtual environment
```bash
pip install virtualenv
python -m venv .venv
```

### Activate virtual environment
#### Windows
```bash
./venv/Scripts/activate
```
#### Linux/Mac
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
Make sure `Papers` directory (`FindMyResearch\Papers`) is created and have research papers in it. The directory should look like [this](#directory).\
If you want to download the research papers (`Papers` directory is automatically created).
```bash
python download_rp.py
```
Run the streamlit application:
```bash
streamlit run app.py
```

## Directory
The directory should look like this after the initial run.\
Ignoring `.venv` files

```
FindMyResearch
+-- .venv
|   +-- <.venv files> ...
+-- .cache
|   +-- hub
    |   +-- <hub files> ...
|   +-- metadata_rp
    |   +-- context.json
    |   +-- metadata.json
|   +-- semantic_rp
    |   +-- semantic_image.dat
    |   +-- semantic_sentence.dat
+-- Papers
|   +-- <Papers files (.pdf)> ...
+-- SearchAlgorithms
|   +-- aisearch.py
|   +-- linear.py
|   +-- sort_filter.py
+-- Tests
|   +-- <Tests files> ...
+-- utils
|   +-- download_paper.py
|   +-- generate_metadata.py
+-- .gitignore
+-- app.py
+-- download_rp.py
+-- README.md
+-- requirements.txt
```

## Working

## Video Demo
