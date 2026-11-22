from invoice_extractor.pdf_extractor import PDFExtractor
from invoice_parsers.invoice_parser import InvoiceParser
from validators.invoice_validator import InvoiceValidator
from validators.confidence_calculator import ConfidenceCalculator
from db_management.database_manager import DatabaseManager


from google import genai
from config import GOOGLE_API_KEY

from models.invoice import Invoice



def main():
    
    client=genai.Client(api_key=GOOGLE_API_KEY)   
    
    # Initialize the PDF extractor, invoice parser, and database manager
    pdf_extractor = PDFExtractor()
    invoice_parser = InvoiceParser(client)
    
    db_manager = DatabaseManager()
    db_manager.create_invoice_table()
    
    print("Database Connection Established")

    # Example usage: extract text from a PDF file
    
    pdf_file_path = "C:/Users/maart/OneDrive/FromaDataSolutions/Belastingdienst/Kw4_2026/Facturen/FM202500903-froma-media_markt.pdf"
    
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            extracted_text = pdf_extractor.extract_text_from_pdf(pdf_file)
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return


    # Parse the extracted text into an invoice object
    invoice = invoice_parser.parse_invoice(extracted_text["text"])
    print(f"Parsed invoice: {invoice}")
    print(invoice_parser._select_model())

    # Validate the invoice
    validator = InvoiceValidator(invoice)
    is_valid = validator.validate()
    print(f"Invoice is valid: {is_valid}")

    # Calculate confidence score
    confidence_calculator = ConfidenceCalculator(invoice, is_valid)
    confidence_score = confidence_calculator.calculate_confidence()
    invoice.confidence = confidence_score
    
    
    print("Invoice confidence =", invoice.confidence)
   
    
    # Store the invoice and its confidence score in the database
    db_manager.insert_invoice(invoice)
    print(f"Inserted invoice with confidence score: {invoice.confidence}")

if __name__ == "__main__":
    main()