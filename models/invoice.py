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
    
    @classmethod
    def from_dict(cls, data: dict):
        # Create an Invoice instance from a dictionary
        return cls(
            supplier=data.get("supplier", ""),
            invoice_number=data.get("invoice_number", ""),
            invoice_date=data.get("invoice_date", ""),
            total_ex_vat=data.get("total_ex_vat", 0.0),
            vat_amount=data.get("vat_amount", 0.0),
            total_inc_vat=data.get("total_inc_vat", 0.0),
            confidence=data.get("confidence", 0.0)
        )
    
    