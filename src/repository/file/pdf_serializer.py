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


    def generate_table_with_cell_constraints(self, data: typing.List[typing.Any],
            with_borders: bool = True):
        table = platypus.Table(data,
                    colWidths=3*0.4*pagesizes.inch,
                    rowHeights=2*0.4*pagesizes.inch,
                )

        if with_borders:
            table.setStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ])

        return table


    def generate_table_without_cell_constraints(self, data:
            typing.List[typing.Any], with_borders:bool = True):
        table = platypus.Table(data)

        if with_borders:
            table.setStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ])

        return table


    def right_align_text(self, text: str) -> styles.ParagraphStyle:
        style: typing.Any = styles.ParagraphStyle(
                    name='text',
                    parent=None,
                    alignment=enums.TA_RIGHT,
                )
        element: typing.Any = platypus.Paragraph(text, style=style)

        return element


    def left_align_text(self, text: str) -> styles.ParagraphStyle:
        style: typing.Any = styles.ParagraphStyle(
                    name='text',
                    parent=None,
                    alignment=enums.TA_LEFT,
                )
        element: typing.Any = platypus.Paragraph(text, style=style)

        return element

    def get_page_break(self):
        return platypus.PageBreak()


    def build_pdf(self, elements: typing.List[typing.Any]) -> typing.Any:
        try:
            self.doc.build(elements)
        except Exception as e:
            import pdb; pdb.set_trace()
            return False
        return True
