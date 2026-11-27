import pandas as pd

class JsonExporter:

    def __init__(self, dataframe):
        
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Expected a pandas DataFrame")
        
        self.dataframe = dataframe

    def export(self) -> str:
        return self.dataframe.to_json(orient="records", indent=4)