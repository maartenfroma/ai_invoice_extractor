import logging
logger = logging.getLogger(__name__)

# Calculate the confidence score for the completeness 
# of an invoice

# Returns a confidence score between 0 and 1 based on the 
# presence of required fields

class ConfidenceCalculator:
    
    # Initialize the confidence calculator with the invoice data
    def __init__(self, invoice: dict):
        self.invoice = invoice

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
            
            #
            if not self.invoice.get(field):
                confidence -= 10

       
        # Return the final confidence score
        
        return confidence 