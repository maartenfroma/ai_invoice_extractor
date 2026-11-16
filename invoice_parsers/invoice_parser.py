import logging

logger = logging.getLogger(__name__)

from google import genai
import json
from models.invoice import Invoice

class InvoiceParser:
    
    MODELS_PREFERRED = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]
    
    def __init__(self, genai_client:genai.Client):
        
        # Initialize the invoice parser
        self.genai_client = genai_client    
        logger.info("InvoiceParser initialized with GenAI client")
        
    # Parse the given invoice text using the GenAI 
    # client and return the parsed data as a dictionary
    
    def parse_invoice(self, invoice_text: str) -> Invoice:
        
        
        if not invoice_text:
            raise ValueError("Invoice text cannot be empty")
        try:
            # Use the GenAI client to parse the invoice text
            response = self.genai_client.models.generate_content(
                model=self._select_model(),
                input_text=invoice_text
            )
            
            # Convert the response from JSON string to dictionary
            parsed_data = json.loads(response.text)
            
            # Log the parsed data for debugging purposes
            logger.info(f"Parsed invoice data: {parsed_data}")
            return Invoice.to_dict(parsed_data)
        
        except Exception as e:
            logger.error(f"Failed to parse invoice: {e}")
            raise Exception(f"Failed to parse invoice: {e}") from e
        
    # Select the appropriate model for parsing invoices based on availability and preference
    # Returns a string representing the selected model
    
    def _select_model(self) -> str:
        
        # Select the preferred model from the list
        available_models=self.genai_client.models()
        
        # Extract the model names from the available models
        list_models=[m.name for m in available_models]
        
        # Log the available models for debugging purposes
        logger.info(f"Available models: {list_models}") 
        for model in self.MODELS_PREFERRED:
            if model in list_models:
                
                # Log the selected model for debugging purposes
                logger.info(f"Selected model: {model}")
                return model
            
        # Return the first available model from the list
        selected_model = list_models[0] if list_models else "gemini-2.5-flash"
        logger.info(f"Selected model: {selected_model}")
        
        # Log the final selected model for debugging purposes
        logger.info(f"Final selected model: {selected_model}")
        
        # Return the final selected model
        return selected_model