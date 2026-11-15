import logging
logger = logging.getLogger(__name__)

import fitz
import json
from google import genai
from google.genai import types
import logging

# PDFExtractor class for extracting text from PDF files and validating invoice data
# This class provides methods to extract text from PDF files and validate invoice data for required fields and correct totals.
# Has the following methods:
# - extract_text_from_pdf: Extracts text from the provided PDF file.
# - validate_invoice_data: Validates the invoice data for required fields and correct totals.

class PDFExtractor:
    def __init__(self, pdf_path: str, genai_client: genai.Client, conn: object):
        self.pdf_path = pdf_path
        self.genai_client = genai_client
        self.conn = conn
        
        logger.info(f"PDFExtractor initialized with PDF path: {pdf_path}")
        logger.info(f"GenAI client initialized: {genai_client}")
        logger.info("PDFExtractor initialization complete")
        
        # Validate the provided PDF path and GenAI client
        logger.info("Validating PDF path and GenAI client") 
        
        # Check if the PDF path and GenAI client are provided
        if not self.pdf_path:
            logger.error("No PDF path provided")
        if not self.genai_client:
            logger.error("No GenAI client provided")    

    # Extract text from the provided PDF file
        logger.info("Extracting text from PDF file")
        
     # Method to extract text from the PDF file
     
    def extract_text_from_pdf(self, file) -> str:
        # Ensure the PDF path is provided
        if not self.pdf_path:
            logger.error("No PDF path provided for text extraction")
            return ""

        logger.info("Starting PDF text extraction")

    
        # Open the PDF file using fitz
        try:
            
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                
                logger.info("PDF file successfully opened with fitz")
                logger.info(f"Number of pages in PDF: {doc.page_count}")
            
                # Log that the PDF file has been successfully opened and the number of pages has been retrieved
                logger.info("PDF file opened and page count retrieved successfully")
            
                 # Initialize an empty string to store the extracted text
                text = ""

                # Iterate through each page in the PDF and extract text
                for page in doc:
                    # Extract text from the current page and append it to the text variable
                    text += page.get_text()
                    
                    # Create metadata for the current page and the 
                    # overall PDF document
                    
                    metadata={
                        
                        "page_count": doc.page_count,
                        "text_length": len(text),
                        "source": "pdf",
                        "file_name": getattr(file, "name", "")
                    }
                    
                    logger.info(f"Metadata for current page: {metadata}")   

                logger.info("Finished PDF text extraction")
                
                # Return the extracted text along with its metadata
                return {"text": text, "metadata": metadata}
            
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            return ""
        
   
    # Validate the invoice data for required fields and correct totals
    #Return a tuple indicating whether the invoice data is valid 
    # and any error messages
    
    def validate_invoice_data(self, invoice_data: dict) -> tuple[bool, str]:
        
        # Initialize a list to store any invoice validation errors
        invoice_errors=[]
    
        # Check if the invoice data is provided
        if not invoice_data:
            return False, "No invoice data provided"

        # Define the required fields for the invoice
        required_fields = ["leverancier", "factuurnummer", "datum", 
                        "totaal_ex_btw", "btw_bedrag", "totaal_inclusief"]

    # Check if all required fields are present in the invoice data
        for field in required_fields:
            if field.lower() not in (key.lower() for key in invoice_data):
                
                logger.error(f"Missing required field: {field}")
                invoice_errors.append(f"Missing required field: {field}")
            
        # Check if the totals match

        try:
            # Extract the relevant totals from the invoice data
            
            ex_btw = float(invoice_data.get("totaal_ex_btw", 0.00))
            btw_bedrag = float(invoice_data.get("btw_bedrag", 0.00))
            totaal_inclusief = float(invoice_data.get("totaal_inclusief", 0.00))

            # Check if the sum of ex_btw and btw_bedrag matches totaal_inclusief
            logger.debug(f"Checking totals: ex_btw={ex_btw}, btw_bedrag={btw_bedrag}, totaal_inclusief={totaal_inclusief}")
            
            # Compare the calculated total with the provided total
            
            if round(ex_btw + btw_bedrag, 2) != round(totaal_inclusief, 2):
                
                logger.error("Mismatch in invoice totals")
                invoice_errors.append("Mismatch in invoice totals")
                
            
        except (ValueError, TypeError, KeyError) as e:
            logger.debug(f"Exception occurred: {e}")
            logger.error(f"Invalid number format: {e}")

            invoice_errors.append(f"Invalid number format: {e}")

            if invoice_errors:
                return False, ", ".join(invoice_errors)

        return True, ""
    
    
   