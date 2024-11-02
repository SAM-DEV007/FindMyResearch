import streamlit as st


@st.cache_resource(show_spinner=False)
def model_load():
    temp_info = st.info('Loading and Verifying Models... Please wait...')

    from utils import generate_metadata
    from SearchAlgorithms import aisearch, linear, sort_filter

    temp_info.empty()

    return generate_metadata, aisearch, linear, sort_filter


@st.cache_resource(show_spinner=False)
def cache_load(text: str = 'Loading and Verifying Cache... Please wait...'):
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


st.title('FindMyResearch')

generate_metadata, aisearch, linear, sort_filter = model_load()
metadata, context, corpus, main_images = cache_load()

search = st.text_input(
    'Search',
    placeholder='Enter search query...',
    max_chars=100,
    autocomplete='off'
)

if search:
    cache_load.clear()
    metadata, context, corpus, main_images = cache_load('Verifying Cache with PDFs... Please wait...')

    search = aisearch.semantic_search(corpus, search)
st.write('Search Results:', search)