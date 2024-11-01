import streamlit as st
st.title('FindMyResearch')
temp_info = st.title('Loading models and cache... Please wait...')

from utils import generate_metadata
generate_metadata.generate_metadata_main()

from SearchAlgorithms import aisearch, linear, sort_filter
linear.generate_context()
aisearch.load_pdf()
aisearch.load_images()


metadata = generate_metadata.load_metadata()
context = linear.load_context()

corpus = load_file('semantic_sentence.dat')
main_images = load_file('semantic_image.dat')


temp_info.empty()