import streamlit as st
import pandas as pd
from db_management.database_manager import DatabaseManager

from helper_file.booking_status import get_status_label

db_manager = DatabaseManager()

st.title("Controle Facturen")

status=st.selectbox("Selecteer de status van de facturen", ["NIEUW","GOEDGEKEURD", "AFGEKEURD",
                                                            "GEBOEKT", "BETAALD"], format_func=get_status_label)

# Fetch and display invoices based on the selected status
if status:
    
    # Get invoices from the database based on the selected status
    invoices = db_manager.get_invoices_by_status(status)
    
    # Display the invoices in a table if any are found
    if invoices:
        
        # Convert the list of invoice dictionaries to a DataFrame for display
        df = pd.DataFrame(invoices)
        
        # Display the total number of invoices for the selected status
        st.write(f"Totaal aantal facturen: {len(invoices)}" )
        
         # Apply the status label to the booking_status column for better readability
        df["booking_status"]=df["booking_status"].apply(get_status_label)
        
        # Reorder columns to show booking_status first for better visibility
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        select_invoice = st.selectbox("Selecteer een factuur", df["invoice_number"])
        
        invoice_number=df[df["invoice_number"]==select_invoice].iloc[0]
       
        st.subheader(f"Details van factuur: {select_invoice}")
        st.write("Leverancier:", invoice_number["supplier"])
        st.write("Factuurnummer:", invoice_number["invoice_number"])
        st.write("Factuurdatum:", invoice_number["invoice_date"])
        st.write("Bedrag:", invoice_number["total_inc_vat"])
        st.write("Status:", invoice_number["booking_status"])
        
        st.metric("Confidence", invoice_number["confidence"])
        
        if status == "AFGEKEURD":
            
         if st.button("✅ Goedkeuren"):
            
                
            db_manager.update_invoice_status(invoice_number["invoice_number"], "GOEDGEKEURD")
            st.success(f"Factuur {select_invoice} is goedgekeurd.")
            
            st.rerun()
        
        
    else:
        st.info(f"Geen facturen gevonden voor de geselecteerde status {status}.") 
        
   
        
        
        
  
        
    
    
    
    
   
    
    
        
    