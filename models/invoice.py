from dataclasses import dataclass, asdict


# Invoice dataclass to store invoice details and related financial information

@dataclass
class Invoice:
    
    supplier: str=""
    invoice_number: str=""
    invoice_date: str=""
    total_ex_vat: float=0.0
    vat_amount: float=0.0
    total_inc_vat: float=0.0
    confidence: float=0.0
    
    # Convert the invoice instance to a dictionary for easy serialization
    def to_dict(self):
        # Convert the dataclass instance to a dictionary
        return asdict(self)
    
    