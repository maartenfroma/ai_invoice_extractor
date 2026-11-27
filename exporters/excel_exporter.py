import pandas as pd
from io import BytesIO


class ExcelExporter:
    
    def __init__(self, dataframe: pd.DataFrame):
        
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Expected a pandas DataFrame")
        
        self.dataframe = dataframe

    def export(self)->bytes:
        
        output = BytesIO()
        self.dataframe.to_excel(output, index=False, engine="openpyxl")
        
        return output.getvalue()