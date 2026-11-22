import logging
import os

logger = logging.getLogger(__name__)

from dotenv import load_dotenv


from google import genai
import json
from models.invoice import Invoice

from custom_exceptions.parser_exceptions import InvalidJSONResponseException, InvoiceParsingException

load_dotenv()

class InvoiceParser:
    
    MODELS_PREFERRED = ["models/gemini-3.8-flash"]
                            
                                    
                        
    def __init__(self, genai_client:genai.Client):
        
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("Missing GOOGLE_API_KEY environment variable")
        
        genai_client = genai.Client(api_key=GOOGLE_API_KEY)
        
        # Initialize the invoice parser
        self.genai_client = genai_client    
        logger.info("InvoiceParser initialized with GenAI client")
        
    # Parse the given invoice text using the GenAI 
    # client and return the parsed data as a dictionary
    
    def parse_invoice(self, invoice_text: str) -> Invoice:
        
        prompt=f"""
        Extract invoice information and return ONLY valid JSON.

        Required fields:

        - supplier
        - invoice_number
        - invoice_date
        - total_ex_vat
        - vat_amount
        - total_inc_vat
        
        IMPORTANT:
        - Return ONLY JSON
        - No markdown
        - No explanations
        - invoice_date must always be in YYYY-MM-DD format
        
        Example:

        {{
            "supplier": "Example BV",
            "invoice_number": "INV-123",
            "invoice_date": "2026-11-03",
            "total_ex_vat": 100.00,
            "vat_amount": 21.00,
            "total_inc_vat": 121.00
        }}

        Invoice Text:

        {invoice_text}
        """
                
        if not prompt:
            raise InvoiceParsingException("Invoice text cannot be empty")
        try:
            
            model = self._select_model()
            # Use the GenAI client to parse the invoice text
            response = self.genai_client.models.generate_content(
                model=model,    
                contents=prompt
            )
            
            response=response.text.strip()
            response = response.replace("```json", "")
            response = response.replace("```", "")
            
            
            # Attempt to parse the response as JSON
            try:
                
                print("\nRAW RESPONSE:")
                print(response)
                print()
                
                # Convert the response from JSON string to dictionary
                parsed_data = json.loads(response)
                
              
            
            # If JSON parsing fails, an exception will be raised and handled above
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON response: {e}")
                raise InvalidJSONResponseException(f"Invalid JSON response: {e}") from e

            # Log the parsed data for debugging purposes
            logger.info(f"Parsed invoice data: {parsed_data}")
            
            # Return the invoice object created from the parsed data
            return Invoice.from_dict(parsed_data)
        
        except Exception as e:
            logger.error(f"Failed to parse invoice: {e}")
            raise InvoiceParsingException(f"Failed to parse invoice: {e}") from e
        
    # Select the appropriate model for parsing invoices based on availability and preference
    # Returns a string representing the selected model
    
    def _select_model(self) -> str:
        
        # Select the preferred model from the list
        available_models=list(self.genai_client.models.list())
        
        for model in available_models:
            print(f"Found model: {model.name}")
        
        # Extract the model names from the available models
        list_models=[model.name for model in available_models]
        
        # Log the available models for debugging purposes
        logger.info(f"Available models: {list_models}") 
        for model in self.MODELS_PREFERRED:
            
            print("Preferred:", self.MODELS_PREFERRED)
            print("Available:", list_models)
            
            if model in list_models:
                
                # Log the selected model for debugging purposes
                logger.info(f"Selected model: {model}")
                return model
            
        # Return the first available model from the list
        selected_model = list_models[0] if list_models else "models/gemini-3.8-flash"
        logger.info(f"Selected model: {selected_model}")
        
        # Log the final selected model for debugging purposes
        logger.info(f"Final selected model: {selected_model}")
        
        # Return the final selected model
        return selected_model