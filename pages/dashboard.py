import streamlit as st
from db_management.database_manager import DatabaseManager

db_manager = DatabaseManager()

st.title("📊 Dashboard")

# Fetch dashboard statistics from the database
stats = db_manager.get_dashboard_stats()

if stats:
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"Facturen: {stats.get('invoice_count', 0)}")
    col2.write(f"Totaalbedrag: {stats.get('total_amount', 0)}")
    col3.write(f"Leveranciers: {stats.get('supplier_count', 0)}")
    col4.write(f"BTW Totaal: {stats.get('vat_total', 0)}")   