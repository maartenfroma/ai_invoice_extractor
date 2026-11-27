import pandas as pd
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class PdfExporter:

    def __init__(self, dataframe: pd.DataFrame):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Expected a pandas DataFrame")

        self.dataframe = dataframe

    def export(self) -> bytes:

        output = BytesIO()

        pdf = canvas.Canvas(
            output,
            pagesize=A4
        )

        width, height = A4

        y = height - 40

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(
            40,
            y,
            "Facturen Export"
        )

        y -= 30

        pdf.setFont("Helvetica", 10)

        for _, row in self.dataframe.iterrows():

            line = " | ".join(
                str(value)
                for value in row
            )

            pdf.drawString(
                40,
                y,
                line
            )

            y -= 20

            if y < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 40

        pdf.save()

        output.seek(0)

        return output.getvalue()