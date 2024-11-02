import streamlit as st
st.set_page_config(layout="wide")

from pathlib import Path
import os


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
        max_chars=100,
        autocomplete='off'
    )

    st.button('Search')
    
    st.divider()

with col_left.container(height=400, border=False):
    options = ('Relevance', 'Title', 'Author', 'Keywords', 'Date', 'Publisher', 'Abstract', 'Doi')
    hide_option = False

    with st.expander('Search Algorithm'):
        search_algorithm = st.selectbox(
            'Search Algorithm',
            options=('Semantic (Text)', 'Semantic (Image)', 'Text', 'Metadata')
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
            ('Increase', 'Decrease')
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
            case 'Metadata':
                total_results = len(metadata)
        
        results_num = [f'All ({total_results})']
        for i in range(1, total_results - 10, 10):
            results_num.append(min(i + 9, total_results))

        filter_results = st.selectbox(
            'Number of Results',
            results_num
        )

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
    
    st.divider()

    st.button('Upload')
    st.write('')

with col_center:
    st.write('Search Results:')

if search:
    metadata, context, corpus, main_images = search_load('Verifying Cache with PDFs... Please wait...')

    match search_algorithm:
        case 'Semantic (Text)':
            search = aisearch.semantic_search(corpus, search)
        case 'Semantic (Image)':
            search = aisearch.image_semantic_search(main_images, search)
        case 'Text':
            search = linear.text_search(search, context)
        case 'Metadata':
            search = linear.metadata_search(search, metadata)

with col_center.container(height=1000, border=False):
    st.write(search)