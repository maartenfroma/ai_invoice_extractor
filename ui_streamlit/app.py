import streamlit as st
from invoice_extractor.pdf_extractor import PDFExtractor
from invoice_parsers.invoice_parser import InvoiceParser
import os
from dotenv import load_dotenv
from validators.invoice_validator import InvoiceValidator
from validators.confidence_calculator import ConfidenceCalculator

from models.invoice import Invoice

from google import genai

from db_management.database_manager import DatabaseManager


import pandas as pd

load_dotenv()

# Initialize the database manager
db_manager = DatabaseManager()

# Create table Invoice
db_manager.create_invoice_table()

print("API KEY:", os.getenv("GOOGLE_API_KEY"))

# Initialize the Google GenAI client with the API key from environment variables
genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))



# Streamlit app for extracting invoice data from uploaded PDF files
st.set_page_config(
    page_title="Factuur AI Piloot",
    page_icon="📄",
    layout="wide"
)

# User interface for uploading PDF invoices and displaying extracted data

st.title("Factuur AI Piloot")
st.caption("Welkom bij de Factuur AI Piloot!")

# Upload PDF invoices
uploaded_files = st.file_uploader("Upload facturen", type=["pdf"], accept_multiple_files=True)


# Process uploaded PDF invoices and extract data
if uploaded_files:
    
    st.success(f"Bestanden succesvol geüpload! Aantal bestanden: {len(uploaded_files)}")
    
    
    # Iterate over each uploaded PDF file and extract invoice data
    for uploaded_file in uploaded_files:
        
       # Display an expander for each uploaded PDF file with its details and extracted data
       with st.expander(f"Bestand: {uploaded_file.name}"):
           
           # Display basic information about the uploaded PDF file
           st.write(f"Bestand: {uploaded_file.name}")
           st.write(f"Grootte: {uploaded_file.size} bytes")
           
           # Initialize the PDF extractor for the uploaded file
           # Returns a dictionary containing the extracted text from the PDF file
           pdf_extractor = PDFExtractor()
           
           # Extract invoice data from the uploaded PDF file
           invoice_data = pdf_extractor.extract_text_from_pdf(uploaded_file)
           
           # Update the invoice object with the invoice data extracted from the PDF file
           # Returns Invoice object created from the parsed data
           parser = InvoiceParser(genai_client)
           parsed_data = parser.parse_invoice(invoice_data)
           
          
           # Initialize the invoice validator with the updated invoice object       
           validator = InvoiceValidator(parsed_data)
           
           # Check for duplicate invoices in the uploaded files
           seen=set()
           
           key=(parsed_data.supplier, parsed_data.invoice_number)
           
           if key in seen:
               st.warning("Duplicate invoice detected in uploaded files.")
               
           seen.add(key)    
           
           
           # Validate the parsed invoice data and calculate confidence score
           # Returns Boolean indicating whether the invoice is valid based on supplier, 
           # invoice number, date, and totals
           is_valid = validator.validate()
           
           # Calculate the confidence score for the invoice based on its validity 
           # and completeness
           # Returns integer number for the confidence.
           confidence = ConfidenceCalculator(parsed_data, is_valid).calculate_confidence()
           
           # Update the invoice object with the calculated confidence score
           parsed_data.confidence = confidence
            
           st.json(parsed_data.to_dict())
           
           st.write("Factuurgegevens met vertrouwensscore:")
           st.write(f"Vertrouwensscore: {confidence}")
           
           # Save the parsed invoice data to the database
           db_manager.insert_invoice(parsed_data)
           
    # Print duplicate invoices in uploaded files
    for supplier, invoice_number in seen:
        st.write(f"Duplicate invoice in uploaded files: Supplier={supplier}, Invoice Number={invoice_number}")
    
    rows=db_manager.get_all_invoices()
    
    invoices_df=pd.DataFrame(rows)
           
    if not invoices_df.empty:
        st.write("Overzicht van alle facturen:")
        st.dataframe(invoices_df,hide_index=True, use_container_width=True)
    else:
        st.write("Geen facturen gevonden.")
        
    st.divider()
    
    st.header("Dashboard Stats")
    stats = db_manager.get_dashboard_stats()
    
    if stats:
        
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"Invoice Count: {stats.get('invoice_count', 0)}")
        col2.write(f"Total Amount: {stats.get('total_amount', 0)}")
        col3.write(f"Supplier Count: {stats.get('supplier_count', 0)}")
        col4.write(f"VAT Total: {stats.get('vat_total', 0)}")
       
     






