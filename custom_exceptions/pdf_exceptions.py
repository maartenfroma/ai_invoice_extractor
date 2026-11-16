
class PDFExtractionError(Exception):
    """Custom exception for errors during PDF text extraction."""
    pass

class PDFValidationError(Exception):
    """Custom exception for errors during PDF validation."""
    pass

class PDFReadError(Exception):
    """Custom exception for errors during PDF reading."""
    pass

class EmptyPDFError(Exception):
    """Custom exception for errors when the PDF is empty."""
    pass


        