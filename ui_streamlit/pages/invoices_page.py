import streamlit as st
import pandas as pd

from db_management.database_manager import DatabaseManager


db = DatabaseManager()

st.title("📋 Factuuroverzicht")

# Fetch all invoices from the database returns a list of rows
# Each row contains the invoice details: ID, Factuurnummer, Datum, Bedrag, Leverancier
rows=db.get_all_invoices()

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True,hide_index=True)
else:
    st.write("Geen facturen gevonden.") 
