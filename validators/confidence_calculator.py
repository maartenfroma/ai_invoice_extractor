import logging
from models.invoice import Invoice
logger = logging.getLogger(__name__)

# Calculate the confidence score for the completeness 
# of an invoice

# Returns a confidence score between 0 and 1 based on the 
# presence of required fields

class ConfidenceCalculator:
    
    # Initialize the confidence calculator with the invoice data
    def __init__(self, invoice: Invoice, is_valid: bool):
        
        # Store the invoice and its validity status for confidence calculation
        self.invoice = invoice
        
        # Store the validity status of the invoice for confidence calculation
        self.is_valid = is_valid

    # Calculate the confidence score for the invoice
    def calculate_confidence(self) -> float:
       

        # Initialize confidence score
        confidence = 100

        if not self.invoice:
            logger.error("Geen factuurgegevens verstrekt")
            return 0

        if not self.invoice.supplier:
           confidence-=10
           logger.debug("Leverancier veld ontbreekt, vertrouwen met 10 verlaagd")
           
        if not self.invoice.invoice_number:
            confidence -= 10
            logger.debug("Factuurnummer veld ontbreekt, vertrouwen met 10 verlaagd")

        if not self.invoice.invoice_date:
            confidence -= 10
            logger.debug("Factuurdatum veld ontbreekt, vertrouwen met 10 verlaagd")

        if not self.invoice.total_ex_vat or self.invoice.total_ex_vat < 0:
            confidence -= 10
            logger.debug("Totaal exclusief BTW veld ontbreekt of is negatief, vertrouwen met 10 verlaagd")

        if self.invoice.vat_amount is None or self.invoice.vat_amount < 0:
            confidence -= 10
            logger.debug("BTW bedrag veld ontbreekt of is negatief, vertrouwen met 10 verlaagd")

        if not self.invoice.total_inc_vat or self.invoice.total_inc_vat < 0:
            confidence -= 10
            logger.debug("Totaal inclusief BTW veld ontbreekt of is negatief, vertrouwen met 10 verlaagd")

        if not self.is_valid:
            confidence -= 25
            logger.debug("Factuur is niet geldig, vertrouwen met 25 verlaagd")

        # Return the final confidence score, 
        # ensuring it is not negative
        
        return max(confidence, 0)