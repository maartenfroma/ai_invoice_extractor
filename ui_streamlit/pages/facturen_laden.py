import streamlit as st
from db_management.database_manager import DatabaseManager
from invoice_extractor.pdf_extractor import PDFExtractor
from invoice_parsers.invoice_parser import InvoiceParser
from validators.invoice_validator import InvoiceValidator
from validators.confidence_calculator import ConfidenceCalculator
from helper_file.booking_status import get_status_label

from google import genai
import os
from dotenv import load_dotenv



load_dotenv()

# Initialize the database manager 
db_manager = DatabaseManager()

# Create the invoice table in the database if it doesn't exist yet  
db_manager.create_invoice_table()

# Initialize the GenAI client
genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("Facturen laden")

st.info("Upload hier uw facturen.")

uploaded_files=st.file_uploader("Upload facturen", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    
    for uploaded_file in uploaded_files:
        with st.expander(f"Uploaded file: {uploaded_file.name}"):
            
            # Extract invoice data from the uploaded PDF file
            # Returns a dictionary containing the extracted invoice data
            pdf_extractor = PDFExtractor()
            invoice_data = pdf_extractor.extract_text_from_pdf(uploaded_file)
            
            # Parse the extracted invoice data into a structured format
            invoice_parser = InvoiceParser(genai_client)
            parsed_invoice = invoice_parser.parse_invoice(invoice_data)
            
            st.write(type(parsed_invoice))
            st.write(parsed_invoice)    
            
            # Validate the parsed invoice data
            validator=InvoiceValidator(parsed_invoice)
            
            # Returns a tuple indicating whether the invoice is valid and any validation error messages
            is_valid, validation_error= validator.validate()
            
            if is_valid:
                
                status="VALIDATED"
                parsed_invoice.booking_status = status
                st.success(get_status_label(status))
                
            else:
                status="REJECTED"
                parsed_invoice.booking_status = status
                st.error(get_status_label(status))
            
            
            # Calculate and display the confidence score for the parsed invoice
            confidence_obj = ConfidenceCalculator(parsed_invoice, is_valid)
            confidence_score = confidence_obj.calculate_confidence()
            
            # Assign the calculated confidence score to the parsed invoice object
            parsed_invoice.confidence = confidence_score
            
            try:
                db_manager.insert_invoice(parsed_invoice)
                st.write(f"factuur geladen: {uploaded_file.name}")
                            
            except Exception as e:
                st.error(f"Factuur laden mislukt: {e}")
            
            st.write(f"Confidence score: {confidence_score}")
            
            st.success("Alle facturen zijn geladen.")
          
            st.write("---")