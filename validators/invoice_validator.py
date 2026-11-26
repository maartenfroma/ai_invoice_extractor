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

class InvoiceValidator: 
    
    db_manager = DatabaseManager()
    
    def __init__(self, invoice: Invoice):
        
        self.invoice = invoice
        
        if not self.invoice:
            raise ValueError("No invoice provided")
    
    # Validate the invoice data and return a 
    # tuple indicating validity and error messages
    
    def validate(self) -> bool: 
        
        # Validate the invoice by checking supplier, invoice number, date, and totals   
        # All are True if valid, False otherwise
        return (self._validate_supplier() and
                self._validate_invoice_number() and
                self._validate_date() and
                self._validate_totals() and
                self._validate_vat_amount() and
                self._validate_no_duplicates())
        
    
    # Validate the supplier field in the invoice
    # Returns True if the supplier field is non-empty, False otherwise
    def _validate_supplier(self) -> bool:
        
        return bool(self.invoice.supplier.strip())
    
    # Validate the invoice number field in the invoice
    # Returns True if the invoice number matches the expected pattern, False otherwise
    def _validate_invoice_number(self) -> bool:
       return bool(re.match(r"^[A-Za-z0-9\-_\/]+$", 
                            self.invoice.invoice_number.strip()))

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
                return True
            except (ValueError, AttributeError):
                pass
            
        return False    
    
    # Validate the totals in the invoice
    # Returns True if the sum of total_ex_vat and vat_amount matches total_inc_vat within a small tolerance, False otherwise            
    def _validate_totals(self) -> bool:
      
            calculated_total = float(self.invoice.total_ex_vat) + float(self.invoice.vat_amount)
            return abs(calculated_total - float(self.invoice.total_inc_vat)) <= 0.01
       
    def _validate_confidence(self) -> bool:
        
        return self.invoice.confidence >= 80.0
    
    
    # Validate the VAT amount in the invoice
    # Returns True if the VAT amount matches the difference between total_inc_vat and total_ex_vat within a small tolerance, False otherwise
    def _validate_vat_amount(self) -> bool:
        
        calculated_vat = float(self.invoice.total_inc_vat) - float(self.invoice.total_ex_vat)
        
        return abs(calculated_vat - float(self.invoice.vat_amount)) <= 0.01
    
    
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
        return (self.invoice.supplier, self.invoice.invoice_number) not in no_duplicates
       