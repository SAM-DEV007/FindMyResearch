import streamlit as st

from utils import generate_metadata
from SearchAlgorithms import aisearch, linear, sort_filter


@st.cache_resource # st.cache_resource.clear()
def start():
    temp_info = st.info('Loading models and cache... Please wait...')

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

metadata, context, corpus, main_images = start()

search = st.text_input('Search')
st.write('Search Results:', search)