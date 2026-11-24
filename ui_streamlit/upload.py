import streamlit as st

st.title("📄 Factuur Upload")


uploaded_files = st.file_uploader("Upload je facturen", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    st.write(f"Bestand geüpload: {uploaded_file.name}")


    st.success("Alle bestanden zijn geüpload.")