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

The uploaded files from the Streamlit application are automatically saved in the `Papers` directory.

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
Make sure `Papers` directory (`FindMyResearch\Papers`) is created and have research papers in it. The directory should look like [this](#directory).

If you want to download the research papers (`Papers` directory is automatically created).
```bash
python download_rp.py
```
Run the streamlit application:
```bash
streamlit run app.py
```

## Directory
The directory should look like this after the initial run.

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
The cache of all the PDFs of the research papers in `Papers` directory are made, and are checked and modified upon every search, sort and filter customization to overcome the discrepancy of unexpected file changes, addition or deletion.

The cache consists of the corpus in text, corpus embeddings, image embeddings and the metadata extraction from the research papers. It ensures that these time taking processes are done only once when the files are added and use the cache to perform search operations swiftly. The cache is updated upon every search for the files added or removed. The cache updation process depends on the files added or removed as it does not modify the other files ensuring that the process takes minimal time.

- Metadata generation\
  [Source code](utils/generate_metadata.py)
  
  The metadata extracted from the papers are the Title, Authors, Publisher, Date issued, Keywords, Abstract and DOI. The metadata is extracted by two methods:
  - DOI
    
    The DOI is extracted from the first page of the paper and cross verified from the internet. The data received from the results is processed and added to the actual metadata of the file. If some of the fields     are not found in this method, the missing fields are generated using the manual method.
  - Manual
    
    The metadata is extracted from the first page of the paper and the actual metadata of the PDF. The Title, Authors, Keywords and Date issued is extracted from the metadata of the PDF. If some of them are not      found, `Roberta Base Squad2` huggingface model is used to extract the Keywords, Date issued and DOI from the paper. Additionally, the Keywords (if not found in previous steps) and Abstract are extracted from     the first page of the PDF.
  
- Search algorithms\
  Source code: [Semantic - Text & Image](SearchAlgorithms/aisearch.py) and [Text & Metadata](SearchAlgorithms/linear.py)

  - Semantic (Text and Image)

    The text (corpus) and images of the papers are converted to embeddings and are matched semantically with the embeddings of the query. The result is in the form of the semantically matched results along with      the score (between 0 to 1) for relevance with the query. The huggingface models, `MiniLLM` for semantic text and `OpenAI CLIP` for semantic image, are used.
  - Text

    The corpus of the papers are matched with the query to get the results.
  - Metadata

    The metadata of the papers are matched with the query to ge the results. It matches the query with every metadata field of the papers.
  - File Search

    The files are searched with the matched names of the PDFs from the `Papers` directory.
  
- Sort and Filter\
  [Source code](SearchAlgorithms/sort_filter.py)

  - Sort
    
    The sorting is based on Relevance and the fields of Metadata of the papers. The Relevance sort is done on the basis of the score received from the Semantic search and is available for the Semantic Search         Algorithms only.

    Special Cases:
    
    Field - Author: It is sorted alphabetically with the first author's name.
    Field - Date: It is sorted according to the date published.

    Any other fields from the above are sorted alphabetically with the whole field details in the metadata of the papers.
    
  - Filter

    The search results are filtered depending on the text entered in the Filter area and the Filter field. The filters are applied to the metadata of the results and then displayed.

## Video Demo
