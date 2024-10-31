def word_search(word: str, pages: list):
    return any(word in page for page in pages)

def sentence_search(sentence: str, pages: list):
    return any(sentence in page for page in pages)

def keyword_search(keyword: str, pdf_metadata: dict):
    return any(keyword in value for value in pdf_metadata['keywords'])