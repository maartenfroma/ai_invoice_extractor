import pandas as pd
import xml.etree.ElementTree as ET


class UblExporter:

    def __init__(self, dataframe: pd.DataFrame):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Expected a pandas DataFrame"
            )

        self.dataframe = dataframe

    def export(self) -> str:

        root = ET.Element("Invoices")

        for _, row in self.dataframe.iterrows():

            invoice = ET.SubElement(
                root,
                "Invoice"
            )

            ET.SubElement(
                invoice,
                "InvoiceNumber"
            ).text = str(
                row.get("invoice_number", "")
            )

            ET.SubElement(
                invoice,
                "Supplier"
            ).text = str(
                row.get("supplier", "")
            )

            ET.SubElement(
                invoice,
                "InvoiceDate"
            ).text = str(
                row.get("invoice_date", "")
            )

            ET.SubElement(
                invoice,
                "TotalExVat"
            ).text = str(
                row.get("total_ex_vat", "")
            )

            ET.SubElement(
                invoice,
                "VatAmount"
            ).text = str(
                row.get("vat_amount", "")
            )

            ET.SubElement(
                invoice,
                "TotalIncVat"
            ).text = str(
                row.get("total_inc_vat", "")
            )

            ET.SubElement(
                invoice,
                "Currency"
            ).text = str(
                row.get("currency", "EUR")
            )

        return ET.tostring(
            root,
            encoding="unicode"
        )