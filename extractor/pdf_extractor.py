import logging
logger = logging.getLogger(__name__)

import fitz

from custom_exceptions.pdf_exceptions import (PDFExtractionError, PDFValidationError, PDFReadError, EmptyPDFError)

# PDFExtractor class for extracting text from PDF files and validating invoice data
# This class provides methods to extract text from PDF files and validate invoice data for required fields and correct totals.
# Has the following methods:
# - extract_text_from_pdf: Extracts text from the provided PDF file.
# - validate_invoice_data: Validates the invoice data for required fields and correct totals.

class PDFExtractor:
    def __init__(self):
        logger.info("Initializing PDFExtractor")

    # Method to extract text from the PDF file
    # Returns a dictionary containing the extracted text 
    # and its metadata.
    
    def extract_text_from_pdf(self, file) -> dict:
        # Ensure the PDF path is provided
        if not file:
            raise PDFReadError("No PDF file provided for text extraction")
            
        logger.info("Starting PDF text extraction")

    
        # Open the PDF file using fitz
        try:
            
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                
                logger.info("PDF file successfully opened with fitz")
                logger.info(f"Number of pages in PDF: {doc.page_count}")
                
                # Check if the PDF has any pages
                if doc.page_count == 0:
                    raise EmptyPDFError("The PDF file is empty")
            
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
                
            
                return {"text": text, "metadata": metadata}
            
        except(EmptyPDFError, PDFReadError) as e :
           raise 
           
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise PDFExtractionError(f"Failed to extract text from PDF: {e}")
        
   
   