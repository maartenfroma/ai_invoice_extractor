import streamlit as st
import pandas as pd
from db_management.database_manager import DatabaseManager

st.title("Leveranciers")

db_manager = DatabaseManager()  # Replace with your actual database manager instance

rows=db_manager.get_supplier_totals()  # Replace with your actual method tofetch suppliers from the database

if rows:
    df = pd.DataFrame(rows, columns=["Leverancier", "Totaal Bedrag"])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.write("Geen leveranciers gevonden.") 
    
supplier=st.selectbox("Selecteer een leverancier", [row[0] for row in rows])

rows=db_manager.get_invoices_by_supplier(supplier)  # Replace with your actual method to fetch invoices for the selected supplier

if rows:
    
    df = pd.DataFrame(rows  )
    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.write("Geen facturen gevonden voor deze leverancier.")