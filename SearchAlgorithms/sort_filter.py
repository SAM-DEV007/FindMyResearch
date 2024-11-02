import re


def sort_search(metadata: dict, results: list, field: str, order: int): # order - 0: increase, 1: decrease
    #title, author, keywords, date, publisher, abstract, doi
    return list(sorted(results, key=lambda k: metadata[k][field], reverse=order))


def sort_relevance(results: dict, order: int): # order - 0: increase, 1: decrease
    # Only for semantic search
    return list(sorted(results, key=results.get, reverse=order))


def filter_search(results: list, metadata: dict, field: str, value: str):
    return [pdf for pdf in results if bool(re.search(value, metadata[pdf][field], flags=re.IGNORECASE))]