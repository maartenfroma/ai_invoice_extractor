import streamlit as st
from db_management.database_manager import DatabaseManager
import plotly.express as px
import pandas as pd


# Initialize the database manager and set up the dashboard page
db_manager = DatabaseManager()

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
    df_invoices = db_manager.get_all_invoices()
    
    if df_invoices:
        st.dataframe(df_invoices, use_container_width=True, hide_index=True)
    
    else:
        st.info("Geen recente facturen gevonden.")
        
    supplier_totals = db_manager.get_supplier_totals()  # Replace with the desired supplier name
    
    df_supplier_totals = pd.DataFrame(supplier_totals, columns=["Supplier", "Total Inc VAT"])   
    
    st.dataframe(df_supplier_totals, use_container_width=True, hide_index=True)
    
    fig = px.bar(df_supplier_totals, x="Supplier", y="Total Inc VAT", title="Total Inc VAT per Supplier")
    st.plotly_chart(fig, use_container_width=True)
        
        
    