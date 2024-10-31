def page_search(search: str, pages: list):
    return bool(re.search(search, '\n'.join((page.get_text("text") for page in pages))))

def metadata_search(keyword: str, metadata: dict, search_type: str):
    return bool(re.search(keyword, metadata[search_type]))