import streamlit as st
st.set_page_config(layout="wide")

from pathlib import Path
import os
import webbrowser
import math


@st.cache_resource(show_spinner=False)
def model_load():
    with col_center:
        temp_info = st.info('Loading and Verifying Models... Please wait...')

    from utils import generate_metadata
    from SearchAlgorithms import aisearch, linear, sort_filter

    temp_info.empty()

    return generate_metadata, aisearch, linear, sort_filter


@st.cache_resource(show_spinner=False)
def cache_load(text: str = 'Loading and Verifying Cache... Please wait...'):
    with col_center:
        temp_info = st.info(text)

    generate_metadata.generate_metadata_main()
    linear.generate_context()
    aisearch.load_pdf()
    aisearch.load_images()

    metadata = generate_metadata.load_metadata()
    context = linear.load_context()

    corpus = aisearch.load_file('semantic_sentence.dat')
    main_images = aisearch.load_file('semantic_image.dat')

    temp_info.empty()

    return metadata, context, corpus, main_images


def search_load(text: str):
    with col_center:
        temp_info = st.info(text)

    generate_metadata.generate_metadata_main()
    linear.generate_context()
    aisearch.load_pdf()
    aisearch.load_images()

    metadata = generate_metadata.load_metadata()
    context = linear.load_context()

    corpus = aisearch.load_file('semantic_sentence.dat')
    main_images = aisearch.load_file('semantic_image.dat')

    temp_info.empty()

    return metadata, context, corpus, main_images


def generate_results(search: list, metadata: dict):
    paper_dir = str(Path(__file__).resolve().parent / 'Papers')
    for pdf in search:
        st.header(metadata[pdf]['title'])
        st.text(", ".join(metadata[pdf]["author"].split(",")))

        if st.button('View PDF', key=pdf):
            if os.path.exists(f'{paper_dir}/{pdf}'):
                webbrowser.open(f'{paper_dir}/{pdf}', new=2)

        if metadata[pdf]['abstract']:
            with st.expander('Abstract'):
                st.write(metadata[pdf]['abstract'])

        with st.expander('Metadata'):
            st.write('')
            st.write('**FILE NAME**')
            st.write(pdf)
            st.write('**FILE LOCATION**')
            st.write(os.path.join(paper_dir, pdf))

            for dat in metadata[pdf]:
                if dat and metadata[pdf][dat]:
                    st.write(f'**{dat.upper()}**')    
                    st.write(metadata[pdf][dat])


if not st.session_state:
    cache_load.clear()
    st.session_state.sample = 0


st.title('FindMyResearch')
st.divider()
col_left, col_center = st.columns([0.2, 0.6], gap="large")

generate_metadata, aisearch, linear, sort_filter = model_load()
metadata, context, corpus, main_images = cache_load()

with col_center:
    search = st.text_input(
        'Search',
        placeholder='Enter search query...',
        max_chars=200,
        autocomplete='off'
    )

    st.button('Search')
    
    st.divider()

with col_left.container(height=400, border=True):
    options = ('Relevance', 'Title', 'Author', 'Keywords', 'Date', 'Publisher', 'Abstract', 'Doi')
    hide_option = False

    with st.expander('Search Algorithm'):
        search_algorithm = st.selectbox(
            'Search Algorithm',
            options=('Semantic (Text)', 'Semantic (Image)', 'Text', 'Metadata', 'File Name'),
            label_visibility='collapsed'
        )

    if 'semantic' not in search_algorithm.lower():
        hide_option = True

    with st.expander('Sort'):
        sort_field = st.selectbox(
            'Sort Field',
            options[1:] if hide_option else options
        )

        sort_order = st.selectbox(
            'Sort Order',
            ('Decrease', 'Increase')
        )

    sort_order = 0 if sort_order == 'Increase' else 1

    with st.expander('Filter'):
        paper_dir = str(Path(__file__).resolve().parent / 'Papers')
        total_results = len(os.listdir(paper_dir))
        
        match search_algorithm:
            case 'Semantic (Text)':
                total_results = len(corpus)
            case 'Semantic (Image)':
                total_results = len(main_images)
        
        results_num = [f'All ({total_results})']
        for i in range(1, total_results - 10, 10):
            results_num.append(min(i + 9, total_results))

        filter_results = st.selectbox(
            'Max. Number of Results',
            results_num
        )
        if isinstance(filter_results, str) and 'All' in filter_results:
            filter_results = total_results
        
        st.divider()

        filter_field = st.selectbox(
            'Filter Field',
            options[1:]
        )

        filter_value = st.text_input(
            'Filter',
            placeholder='Enter filter text...',
            max_chars=100,
            autocomplete='off'
        )

        st.button('Filter')
    
    files = st.file_uploader('Research Paper', type=('pdf'), accept_multiple_files=True)
    if files:
        for file in files:
            if file.type == 'application/pdf':
                with open(f'{paper_dir}/{file.name}', 'wb') as f:
                    f.write(file.getvalue())

    st.write('')

with col_center:
    st.write('Search Results:')

if search:
    metadata, context, corpus, main_images = search_load('Verifying Cache with PDFs... Please wait...')
    semantic, normal = False, False

    match search_algorithm:
        case 'Semantic (Text)':
            search = aisearch.semantic_search(corpus, search, num_search=filter_results)
            if sort_field == 'Relevance':
                semantic = True
            else:
                normal = True
        case 'Semantic (Image)':
            search = aisearch.image_semantic_search(main_images, search, num_search=filter_results)
            if sort_field == 'Relevance':
                semantic = True
            else:
                normal = True
        case 'Text':
            search = linear.text_search(context, search)
            normal = True
        case 'Metadata':
            search = linear.metadata_search_all(metadata, search)
            normal = True
        case 'File Name':
            search = sort_filter.file_search(metadata, search)
            normal = True

    if semantic:
        search = sort_filter.sort_relevance(search, sort_order)
    if normal:
        search = sort_filter.sort_search(metadata, search, sort_field.lower(), sort_order)[:filter_results + 1]

    if filter_value:
        search = sort_filter.filter_search(search, metadata, filter_field.lower(), filter_value)

with col_center:
    num_pages = st.selectbox(
        'Number of Results per Page',
        [10, 20, 30, 40, 50]
    )

    pages = math.ceil(len(search) / num_pages)

    page_holder = st.selectbox(
        'Select Page',
        [f'Page {i}' for i in range(1, pages + 1)]
    )

with col_center.container(height=700, border=True):
    if page_holder:
        current_page = int(page_holder[-1])
        search = search[(current_page - 1) * num_pages:current_page * num_pages]

        generate_results(search, metadata)