import streamlit as st
import pandas as pd

from db_management.database_manager import DatabaseManager

# Initialize the database manager and ensure the invoice table exists
db = DatabaseManager()

# make sure the invoice table exists before fetching invoices
db.create_invoice_table()

st.title("📋 Factuuroverzicht")

# Fetch all invoices from the database returns a list of rows
# Each row contains the invoice details: ID, Factuurnummer, Datum, Bedrag, Leverancier
rows, headers=db.get_all_invoices()

if rows:
    df = pd.DataFrame(rows, columns=headers)
    st.dataframe(df,use_container_width=True,hide_index=True)
else:
    st.write("Geen facturen gevonden.") 

# Search for invoices based on supplier or invoice number
search_term = st.selectbox(
    "Zoek facturen op leverancier of factuurnummer",
    options=[""] + [str(row[4]) for row in rows] + [str(row[1]) for row in rows]
)


if search_term:
    filtered_rows = [row for row in rows if search_term.lower() in str(row).lower()]
    if filtered_rows:
        df = pd.DataFrame(filtered_rows, columns=headers)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("Geen facturen gevonden voor de zoekterm.")
    

