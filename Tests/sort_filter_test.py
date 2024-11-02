import metadata_main
import sentence_image_combine

import re


def sort_search(metadata: dict, results: list, field: str, order: int): # order - 0: increase, 1: decrease
    #title, author, keywords, date, publisher, abstract, doi
    return list(sorted(results, key=lambda k: metadata[k][field], reverse=order))


def sort_relevance(results: list, order: int): # order - 0: increase, 1: decrease
    # Only for semantic search
    return list(sorted(results, key=results.get, reverse=order))


def filter_search(metadata: dict, field: str, value: str):
    return [pdf for pdf in metadata if bool(re.search(value, metadata[pdf][field], flags=re.IGNORECASE))]


metadata = metadata_main.load_metadata()

sentence_image_combine.load_pdf()
corpus = sentence_image_combine.load_file('semantic_sentence.dat')

query = 'machine learning'
pdfs = sentence_image_combine.semantic_search(corpus, query, num_search=10)

print(pdfs)
print()
print(sort_relevance(pdfs, 1))
print()
print(sort_search(metadata, pdfs, 'title', 1))
print()
print(filter_search(metadata, 'author', 'Zhang'))