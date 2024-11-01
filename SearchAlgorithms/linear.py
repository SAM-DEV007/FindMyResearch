import re


def pdf_search(search: str, context: str):
    return bool(re.search(search, context, flags=re.IGNORECASE))

def metadata_search(keyword: str, sub_metadata: dict, search_type: str):
    return bool(re.search(keyword, sub_metadata[search_type], flags=re.IGNORECASE))