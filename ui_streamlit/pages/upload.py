import streamlit as st
from db_management.database_manager import DatabaseManager

st.title("Facturen laden")

st.info("Upload hier uw facturen.")

uploaded_files=st.file_uploader("Upload facturen", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    
    for uploaded_file in uploaded_files:
        with st.expander(f"Uploaded file: {uploaded_file.name}"):
            st.write(f"Processing {uploaded_file.name}...")
         
            