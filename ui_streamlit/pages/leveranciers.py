import streamlit as st
import pandas as pd
from db_management.database_manager import DatabaseManager
from models.invoice import Invoice

# Page to display suppliers and their total invoice amounts
st.title("Leveranciers")

# Initialize the database manager
db_manager = DatabaseManager()  

# Fetch the supplier totals from the database
supplier_rows=db_manager.get_supplier_totals()  

# Display the supplier totals and allow the user to select a supplier
if supplier_rows:
    
    # Create a DataFrame from the supplier rows for display and selection   
    supplier_df = pd.DataFrame(supplier_rows)
    supplier_df.rename(
        columns={
            "supplier": "Leverancier",
            "total_inc_vat": "Totaal Bedrag"
        }
    )
    st.dataframe(supplier_df, use_container_width=True, hide_index=True)
    
    # Display the supplier details section
    st.subheader("Leverancier Details")
    
    # Allow the user to select a supplier to view details for
    supplier = st.selectbox("Selecteer een leverancier", supplier_df["supplier"])
    
    st.subheader(f"Facturen voor {supplier}")
    
    
    invoice_rows=db_manager.get_invoices_by_supplier(supplier)
    
    if invoice_rows:
        
        # Fetch the invoice headers for the DataFrame columns   
        invoice_df = pd.DataFrame(invoice_rows)
        st.dataframe(invoice_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("Geen facturen gevonden voor deze leverancier.")    
        
        
else:
    st.warning("Geen leveranciers gevonden.")
        
