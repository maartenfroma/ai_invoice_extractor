import logging
import re
from datetime import datetime
from wsgiref import headers
from models.invoice import Invoice

from db_management.database_manager import DatabaseManager

logger = logging.getLogger(__name__)



# Validate the invoice data for required fields and correct totals
#Return a tuple indicating whether the invoice data is valid 
# and any error messages

# Contains the following methods
#* validate
#* _validate_supplier
#* _validate_invoice_number
#* _validate_date
#* _validate_totals
#* _validate_confidence
#* _validate_vat_amount
#* _validate_no_duplicates
#* _validate_category

class InvoiceValidator: 
    
    db_manager = DatabaseManager()
    
    def __init__(self, invoice: Invoice):
        
        self.invoice = invoice
        
        if not self.invoice:
            raise ValueError("No invoice provided")
    
    # Validate the invoice data and return a 
    # tuple indicating validity and error messages
    
    def validate(self) -> tuple: 
        
        # Validate the invoice by checking supplier, invoice number, date, and totals   
        # All are True if valid, False otherwise
        validations = [
            self._validate_supplier(),
            self._validate_invoice_number(),
            self._validate_date(),
            self._validate_totals(),
            self._validate_vat_amount(),
            self._validate_no_duplicates()
        ]
        
        # Collect all validation errors from the individual validation methods
        validation_errors = []
        
        # Iterate through the validation results and collect errors
        for valid, error in validations:
            
            # If the validation result is not valid, collect the error message
            if not valid:
                validation_errors.append(error)
                
        # If there are any validation errors, return False with the concatenated error messages
        if validation_errors:
            
            # Return False along with all collected validation error messages
            return False, "; ".join(validation_errors)
        
        # If there are no validation errors, return True with an empty error message
        return True, ""
        
    
    # Validate the supplier field in the invoice
    # Returns True if the supplier field is non-empty, False otherwise
    def _validate_supplier(self) -> bool:
        
        if not self.invoice.supplier.strip():
            return False, "Supplier is empty"
        return True, ""
    
    # Validate the invoice number field in the invoice
    # Returns True if the invoice number matches the expected pattern, False otherwise
    def _validate_invoice_number(self) -> bool:
        
        
        if not re.match(r"^[A-Za-z0-9\-_\/]+$", self.invoice.invoice_number.strip()):
            return False, "Invalid invoice number"
        return True, ""

    # Validate the invoice date field in the invoice
    # Returns True if the invoice date is in the correct format, False otherwise
    def _validate_date(self) -> bool:
        date_formats=[
            "%Y-%m-%d",
                    "%d %b %Y",
                    "%d %B %Y"
                ]
        for fmt in date_formats:
            try:
                datetime.strptime(self.invoice.invoice_date.strip(), fmt)
                return True, ""
            except (ValueError, AttributeError):
                pass
            
        return False, "Invalid date format"
    
    # Validate the totals in the invoice
    # Returns True if the sum of total_ex_vat and vat_amount matches total_inc_vat within a small tolerance, False otherwise            
    def _validate_totals(self) -> bool:
        calculated_total = float(self.invoice.total_ex_vat) + float(self.invoice.vat_amount)
        if not abs(calculated_total - float(self.invoice.total_inc_vat)) <= 0.01:
            return False, "Totals do not match"
        return True, ""
       
    def _validate_confidence(self) -> bool:
        
        if self.invoice.confidence < 80.0:
            return False, "Confidence below threshold"
        return True, ""
    
    
    # Validate the VAT amount in the invoice
    # Returns True if the VAT amount matches the difference between total_inc_vat and total_ex_vat within a small tolerance, False otherwise
    def _validate_vat_amount(self) -> bool:
        
        calculated_vat = float(self.invoice.total_inc_vat) - float(self.invoice.total_ex_vat)
        
        if not abs(calculated_vat - float(self.invoice.vat_amount)) <= 0.01:
            return False, "VAT amount does not match"
        return True, ""
        
    
    
    # Validate if the invoice is a duplicate in the database
    # Returns false if a duplicate is found, True otherwise
    def _validate_no_duplicates(self) -> bool:
        
        db_manager = self.db_manager
        
        # Retrieve all invoices from the database to check for duplicates
        rows,_ = db_manager.get_all_invoices()
        
        no_duplicates=set()
        
        for row in rows:
            no_duplicates.add((row["supplier"], row["invoice_number"]))
        
        # True if no duplicate is found, False otherwise
        if not (self.invoice.supplier, self.invoice.invoice_number) in no_duplicates:
            return True, ""
        
        return False, "Duplicate invoice found"
    
    def _validate_category(self) -> bool:
        
        # Returns True if the category field is non-empty, False otherwise
        if not bool(self.invoice.category.strip()):
            return False, "No category specified"
        
        return True, ""
    
    def get_validated_invoice(self):
        try:
            query="""
            SELECT * FROM invoices
            WHERE booking_status = 'VALIDATED' 
            ORDER BY invoice_date DESC
            """
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                
            return rows
            
        except Exception as e:
            logger.error(
                f"Failed to get validated invoices: {e}"
            )

        raise RuntimeError(
            f"Failed to get validated invoices: {e}"
        ) from e
       