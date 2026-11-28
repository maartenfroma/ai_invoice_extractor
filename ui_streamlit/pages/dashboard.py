import streamlit as st
from db_management.database_manager import DatabaseManager
import plotly.express as px
import pandas as pd


# Initialize the database manager and set up the dashboard page
db_manager = DatabaseManager()

try:
    db_manager.create_invoice_table()
    
except Exception as e:
    st.error(f"Kon geen factuurtabel aanmaken: {e}")

# Set up the dashboard page title and layout
st.title("📊 Dashboard")

# Fetch dashboard statistics from the database
stats = db_manager.get_dashboard_stats()

# Display the dashboard statistics in columns if available
if stats:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Facturen", stats.get("invoice_count", 0))
        
    with col2:
        st.metric("Totaalbedrag", stats.get("total_inc_vat", 0))
        
    with col3:
        st.metric("Leveranciers", stats.get("supplier_count", 0))
        
    with col4:
        st.metric("BTW Totaal", stats.get("vat_total", 0))
        
        
    st.subheader("📄 Recente facturen")
    
    # Fetch all invoices from the database returns rows as a list of dictionaries
    rows, headers = db_manager.get_all_invoices()
    df_invoices = pd.DataFrame(rows, columns=headers)
    
    if not df_invoices.empty:
        st.dataframe(df_invoices, use_container_width=True, hide_index=True)
    
    else:
        st.info("Geen recente facturen gevonden.")
        
   
        
    