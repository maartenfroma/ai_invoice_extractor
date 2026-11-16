
class PDFError(Exception):
    """Base class for all PDF-related errors."""
    pass
    
class PDFExtractionError(PDFError):
    """Custom exception for errors during PDF text extraction."""
    pass

class PDFValidationError(PDFError):
    """Custom exception for errors during PDF validation."""
    pass

class PDFReadError(PDFError):
    """Custom exception for errors during PDF reading."""
    pass

class EmptyPDFError(PDFError):
    """Custom exception for errors when the PDF is empty."""
    pass


        