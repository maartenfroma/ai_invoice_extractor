import logging
logger = logging.getLogger(__name__)



# Validate the invoice data for required fields and correct totals
#Return a tuple indicating whether the invoice data is valid 
# and any error messages

class InvoiceValidator:     
    
    def __init__(self, invoice: dict):
        
        self.invoice = invoice
    
    # Validate the invoice data and return a 
    # tuple indicating validity and error messages
    
    def validate(self) -> tuple[bool, str]:
        # Initialize a list to store any invoice validation errors
        invoice_errors=[]

        # Check if the invoice data is provided
        if not self.invoice:
            return False, "No invoice data provided"

        # Define the required fields for the invoice
        required_fields = ["leverancier", "factuurnummer", "datum", 
                        "totaal_ex_btw", "btw_bedrag", "totaal_inclusief"]

    # Check if all required fields are present in the invoice data
        for field in required_fields:
            if field.lower() not in (key.lower() for key in self.invoice):
                
                logger.error(f"Missing required field: {field}")
                invoice_errors.append(f"Missing required field: {field}")
            
        # Check if the totals match

        try:
            # Extract the relevant totals from the invoice data
            
            ex_btw = float(self.invoice.get("totaal_ex_btw", 0.00))
            btw_bedrag = float(self.invoice.get("btw_bedrag", 0.00))
            totaal_inclusief = float(self.invoice.get("totaal_inclusief", 0.00))

            # Check if the sum of ex_btw and btw_bedrag matches totaal_inclusief
            logger.debug(f"Checking totals: ex_btw={ex_btw}, btw_bedrag={btw_bedrag}, totaal_inclusief={totaal_inclusief}")
            
            # Compare the calculated total with the provided total
            
            if abs((ex_btw + btw_bedrag) - totaal_inclusief) > 0.01:
                
                logger.error("Mismatch in invoice totals")
                invoice_errors.append("Mismatch in invoice totals")
                
            
        except (ValueError, TypeError, KeyError) as e:
            logger.debug(f"Exception occurred: {e}")
            logger.error(f"Invalid number format: {e}")

            invoice_errors.append(f"Invalid number format: {e}")

        if invoice_errors:
            return False, ", ".join(invoice_errors)

        return True, ""


