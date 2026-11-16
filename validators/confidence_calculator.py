import logging
logger = logging.getLogger(__name__)

# Calculate the confidence score for the completeness 
# of an invoice

# Returns a confidence score between 0 and 1 based on the 
# presence of required fields

class ConfidenceCalculator:
    
    # Initialize the confidence calculator with the invoice data
    def __init__(self, invoice: dict, is_valid: bool):
        self.invoice = invoice
        self.is_valid = is_valid

    def calculate_confidence(self) -> float:
        # Initialize confidence score
        confidence = 100

        if not self.invoice:
            logger.error("No invoice data provided")
            return 0

        required_fields = ["leverancier", "factuurnummer", "datum", 
                           "totaal_ex_btw", "btw_bedrag", "totaal_inclusief"]

        # Check for presence of required fields
        for field in required_fields:
            
            logger.debug(f"Checking presence of field: {field}")
            
            # If the field is missing, decrease confidence by 10
            if not self.invoice.get(field):
                confidence -= 10

        # Adjust confidence based on the validity of the invoice
        # This means that if the invoice is not valid, 
        # the confidence score is reduced by 25
        
        if not self.is_valid:
            confidence -= 25
        
        return confidence 