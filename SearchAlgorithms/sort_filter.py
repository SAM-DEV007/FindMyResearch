import re


def sort_search(metadata: dict, results: list, field: str, order: int): # order - 0: increase, 1: decrease
    #title, author, keywords, date, publisher, abstract, doi
    sorted_results = {}
    for pdf in metadata:
        sorted_results[pdf] = metadata[pdf][field]

    return list(sorted(results, key=lambda k: metadata[k][field], reverse=order))


def sort_relevance(results: list, order: int): # order - 0: increase, 1: decrease
    # Only for semantic search
    return list(sorted(results, key=results.get, reverse=order))


def filter_search(metadata: dict, field: str, value: str):
    return [pdf for pdf in metadata if bool(re.search(value, metadata[pdf][field], flags=re.IGNORECASE))]