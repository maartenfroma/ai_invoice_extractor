import pandas as pd
from datetime import datetime

class CSVExporter:
    
    def __init__(self, dataframe: pd.DataFrame):
        
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Expected a pandas DataFrame")
        
        self.dataframe = dataframe

    def export(self)->str:
        
        return self.dataframe.to_csv(index=False)