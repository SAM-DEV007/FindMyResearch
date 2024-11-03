import re
from datetime import datetime


def sort_search(metadata: dict, results: list, field: str, order: int): # order - 0: increase, 1: decrease
    #title, author, keywords, date, publisher, abstract, doi
    match field:
        case 'author':
            sort = list(sorted(results, key=lambda k: metadata[k][field].split(',')[0], reverse=order))
        case 'date':
            sort = list(sorted(results, key=lambda k: datetime.strptime(metadata[k][field], '%d-%m-%Y'), reverse=order))
        case _:
            sort = list(sorted(results, key=lambda k: metadata[k][field].lower(), reverse=order))

    return sort


def sort_relevance(results: dict, order: int): # order - 0: increase, 1: decrease
    # Only for semantic search
    return list(sorted(results, key=results.get, reverse=order))


def filter_search(results: list, metadata: dict, field: str, value: str):
    return [pdf for pdf in results if bool(re.search(value, metadata[pdf][field], flags=re.IGNORECASE))]


def file_search(metadata: dict, value: str):
    return [pdf for pdf in metadata if bool(re.search('.*'.join(value.split()), pdf, flags=re.IGNORECASE))]