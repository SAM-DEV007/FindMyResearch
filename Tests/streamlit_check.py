import streamlit as st

st.title('FindMyResearch_Test')
t = st.info('Loading models and creating cache... Please wait...')

import streamlit_check_module
streamlit_check_module.main()

t.empty()

# streamlit run Tests/streamlit_check.py