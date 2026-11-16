import logging

logger = logging.getLogger(__name__)

from google import genai
import json

class InvoiceParser:
    
    def __init__(self, genai_client):
        
        # Initialize the invoice parser
        self.genai_client = genai_client    
        logger.info("InvoiceParser initialized with GenAI client")