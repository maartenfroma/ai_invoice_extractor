import logging
import re
from datetime import datetime
from models.invoice import Invoice
logger = logging.getLogger(__name__)



# Validate the invoice data for required fields and correct totals
#Return a tuple indicating whether the invoice data is valid 
# and any error messages

class InvoiceValidator:     
    
    def __init__(self, invoice: Invoice):
        
        self.invoice = invoice
        
        if not self.invoice:
            raise ValueError("No invoice provided")
    
    # Validate the invoice data and return a 
    # tuple indicating validity and error messages
    
    def validate(self) -> bool:
        
        # Use the provided invoice or fall back to the instance's invoice
        if not self.invoice:
            raise ValueError("No invoice provided") 
        
        # Fall back to the instance's invoice if no invoice is provided
        return (self._validate_supplier() and
                self._validate_invoice_number() and
                self._validate_date() and
                self._validate_totals())
        
    
        
        
    
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