from dataclasses import dataclass, asdict


# Invoice dataclass to store invoice details and related financial information

@dataclass
class Invoice:
    
    # Supplier details
    supplier: str=""
    supplier_vat_number: str=""
    supplier_chamber_of_commerce: str=""
    
    # Invoice details
    invoice_number: str=""
    invoice_date: str=""
    due_date: str | None=None
    
    currency: str="EUR"
    
    total_ex_vat: float=0.0
    vat_amount: float=0.0
    total_inc_vat: float=0.0
    
    vat_code: str=""
    
    category: str=""
    ledger_account: str=""
    
    # Accounting details
    cost_center:str=""
    project_code: str=""
    
    # Metadata
    confidence: int=0   
    booking_status: str="PENDING"
 
    # Source of the invoice data
    source_file: str=""
    
    
    
    # Convert the invoice instance to a dictionary for easy serialization
    
    def to_dict(self):
        # Convert the dataclass instance to a dictionary
        return asdict(self)
   
    @classmethod
    def from_dict(cls, data: dict):
        # Create an Invoice instance from a dictionary
        
        return cls(
            
            # Supplier details
            supplier=data.get("supplier", ""),
            supplier_vat_number=data.get("supplier_vat_number", ""),
            supplier_chamber_of_commerce=data.get("supplier_chamber_of_commerce", ""),
            
            # Invoice details
            invoice_number=data.get("invoice_number", ""),
            invoice_date=data.get("invoice_date", ""),
            due_date=data.get("due_date", None),
            currency=data.get("currency", "EUR"),
            
            # Financial details
            total_ex_vat=data.get("total_ex_vat", 0.0),
            vat_amount=data.get("vat_amount", 0.0),
            total_inc_vat=data.get("total_inc_vat", 0.0),
            vat_code=data.get("vat_code", ""),
            
            # Accounting details
            category=data.get("category", ""),
            ledger_account=data.get("ledger_account", ""),
            cost_center=data.get("cost_center", ""),
            project_code=data.get("project_code", ""),
            
            # Metadata
            confidence=data.get("confidence", 0),
            booking_status=data.get("booking_status", ""),
            
            # Source of the invoice data
            source_file=data.get("source_file", "")
        )
        
    
    
    