import os
import typing
import logging

from reportlab import platypus
from reportlab.lib import colors, pagesizes, styles, enums

from repository.file import BaseFileRepo

class PdfSerializer(metaclass=BaseFileRepo):
    """
    Serializer class for serializing data in a specific format to a pdf.
    """
    def __init__(self, logger: logging.Logger, output_dir: str):
        self.logger = logger
        self.output_dir = output_dir

    def read(self, fname: str):
        pass

    def write(self, fname: str):
        pass

    def init_pdf(self, fname: str):
        filename: str = os.path.join(
                    self.output_dir,
                    fname,
                )
        doc = platypus.SimpleDocTemplate(filename,
                pagesize=pagesizes.landscape(pagesizes.A4))

        self.doc = doc
        return doc


    def generate_table(self, elements: typing.List[typing.Any],
            data: typing.List[typing.Any], with_page_break: bool = True):
        table = platypus.Table(data,
                    colWidths=3*0.4*pagesizes.inch,
                    rowHeights=2*0.4*pagesizes.inch,
                )
        table.setStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ])

        elements.append(table)

        if with_page_break:
            elements.append(platypus.PageBreak())

        return elements
