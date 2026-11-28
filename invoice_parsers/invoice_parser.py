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
        logger.info("Initialiseren van InvoiceParser")
        
    # Parse the given invoice text using the GenAI 
    # client and return the parsed data as a dictionary
    
    def parse_invoice(self, invoice_text: str) -> Invoice:
        
        prompt=f"""
        Extraheer de factuurinformatie en retourneer ALLEEN geldige JSON.

        Vereiste velden:

        - supplier
        - invoice_number
        - invoice_date
        - total_ex_vat
        - vat_amount
        - total_inc_vat
        
        BELANGRIJK:
        - Retourneer ALLEEN JSON
        - Geen markdown
        - Geen uitleg
        - invoice_date moet altijd in YYYY-MM-DD formaat zijn
        
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
            
            print("\nAntwoord:")
            print(response)
            print()
            
            # Convert the response from JSON string to dictionary
            parsed_data = json.loads(response)
            
            
        
        # If JSON parsing fails, an exception will be raised and handled above
        except json.JSONDecodeError as e:
            logger.error(f"Foute JSON response: {e}")
            raise InvalidJSONResponseException(f"Foute JSON response: {e}") from e

        # Log the parsed data for debugging purposes
        logger.info(f"Geparste factuurdata: {parsed_data}")
        
        # Return the invoice object created from the parsed data
        return Invoice.from_dict(parsed_data)
    
        
    # Select the appropriate model for parsing invoices based on availability and preference
    # Returns a string representing the selected model
    
    def _select_model(self) -> str:
        
        # Select the preferred model from the list
        available_models=list(self.genai_client.models.list())
        
        for model in available_models:
            print(f"Gevonden model: {model.name}")
        
        # Extract the model names from the available models
        list_models=[model.name for model in available_models]
        
        # Log the available models for debugging purposes
        logger.info(f"Beschikbare modellen: {list_models}") 
        for model in self.MODELS_PREFERRED:
            
            print("Voorkeur:", self.MODELS_PREFERRED)
            print("Beschikbaar:", list_models)
            
            if model in list_models:
                
                # Log the selected model for debugging purposes
                logger.info(f"Geselecteerd model: {model}")
                return model
            
        # Return the first available model from the list
        selected_model = list_models[0] if list_models else "models/gemini-3.8-flash"
        logger.info(f"Geselecteerd model: {selected_model}")
        
        # Log the final selected model for debugging purposes
        logger.info(f"Definitief geselecteerd model: {selected_model}")
        
        # Return the final selected model
        return selected_model