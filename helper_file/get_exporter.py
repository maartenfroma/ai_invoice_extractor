
import pandas as pd

from exporters.json_exporter import JsonExporter
from exporters.ubl_exporter import UblExporter
from exporters.csv_exporter import CSVExporter
from exporters.pdf_exporter import PdfExporter
from exporters.twinfield_exporters import TwinfieldExporter
from exporters.excel_exporter import ExcelExporter
from exporters.exact_exporter import ExactExporter

#  Returns an instance of the appropriate exporter class based on the exporter_type. Raises ValueError if the type is unknown.
def get_exporter(exporter_type: str, df: pd.DataFrame):
    
    #  Dictionary mapping exporter types to their corresponding classes.
    exporters={
        
        "json": JsonExporter,
        "ubl": UblExporter,
        "csv": CSVExporter,
        "pdf": PdfExporter,
        "twinfield": TwinfieldExporter,
        "excel": ExcelExporter,
        "exact": ExactExporter
    }
    
    #  Get the exporter class from the dictionary based on the exporter_type.
    if exporter_type.lower() in exporters:
        
        exporter_class=exporters.get(exporter_type.lower(), df)
        
        if exporter_class is None:
            raise ValueError(f"Unknown exporter type: {exporter_type}")
    else:
        raise ValueError(f"Unknown exporter type: {exporter_type}")
        
    #  Return an instance of the exporter class initialized with the DataFrame.
    return exporter_class(df)
    