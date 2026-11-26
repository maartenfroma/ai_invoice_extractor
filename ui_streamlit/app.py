import streamlit as st

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Factuuur AI Piloot",
    page_icon="📊",
    layout="wide"
    )

# Set up the dashboard page for displaying statistics and recent invoices
dash=st.Page("pages/dashboard.py",title="Dashboard", icon="📊")

# Set up the upload page for loading invoices
upload_page = st.Page("pages/facturen_laden.py", title="Facturen laden", icon="📤") 

# Set up the invoice page for viewing invoices
invoices_page = st.Page("pages/facturen.py", title="Facturen", icon="📄")

supplier_page = st.Page("pages/leveranciers.py", title="Leveranciers", icon="🏢")

# Set up the navigation for switching between pages
pg=st.navigation([dash, upload_page, invoices_page, supplier_page])

pg.run()