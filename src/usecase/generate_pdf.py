import os
import time
import uuid
import typing
import logging
from datetime import datetime

from reportlab import platypus
from reportlab.lib import colors, pagesizes, styles, enums

import models
from usecase import BaseUseCase
from repository.file import PdfSerializer

class GenerateCyclePdfUsecase(metaclass=BaseUseCase):
    def __init__(self, logger: logging.Logger,
            output_dir: str,
            pdf_serializer: PdfSerializer,):
        self.logger = logger
        self.output_dir = output_dir
        self.pdf_serializer = pdf_serializer
        self.elements = []

    def _init_pdf(self):
        #TODO: move folder to constants
        filename: str = os.path.join(
                    self.output_dir,
                    f'{uuid.uuid1()}.pdf',
                )
        doc = platypus.SimpleDocTemplate(filename,
                pagesize=pagesizes.landscape(pagesizes.A4))

        self.doc = doc
        return doc


    def get_page_headers(self):
        page_headers: typing.List[str] = [
                    'Exercise',
                    'Equipment',
                    'Mass(kg)',
                    'Sets',
                    'Set Duration(s)',
                    'Reps/Set',
                    'Rest Duration(s)',
                    'Work Capacity',
                ]
        return page_headers


    def generate_first_page(self, cycle: models.Programme):
        """
        Builds the first page of the PDF. Check the sample pdf for the format
        of the generated pdf.

        """
        programme_days: typing.Dict = {}
        dex_max: int = 0

        sessions = cycle.sessions

        # since the pdf has to be populated in a row first format i.e., a row has
        # to be completely filled out before a moving onto the next one,
        # we find out the maximum number of rows that need to be filled out so
        # that this can be iterated on a at a later point in time.
        for k in sessions.keys():
            day: str = time.strftime("%A", time.localtime(int(k)))
            if programme_days.get(day) is not None:
                for e in sessions[k].keys():
                    if not e in programme_days[day]:
                        programme_days[day].append(e)

            else:
                programme_days[day] = [v for v in sessions[k].keys()]

            if len(programme_days[day]) > dex_max:
                dex_max = len(programme_days[day])

        days: typing.List[str] = [
                    'Monday',
                    'Tuesday',
                    'Wednesday',
                    'Thursday',
                    'Friday',
                    'Saturday',
                    'Sunday',
                ]

        rows = [days,]
        dex_idx: int = 0
        while dex_idx < dex_max:
            row = list()
            for d in days:
                dexs: typing.List[str] = programme_days.get(d, [])
                dex: str = '-'
                if len(dexs) > 0:
                    if len(dexs) > dex_idx:
                        dex = dexs[dex_idx]
                row.append(dex)
            rows.append(row)
            dex_idx += 1

        table = self.pdf_serializer.generate_table_with_cell_constraints(rows, True)
        self.elements.append(table)
        self.elements.append(self.pdf_serializer.get_page_break())


    def prepare_page(self, timestamp: int, rows: typing.List[typing.Any]):
        sheet_date: str = str(datetime.fromtimestamp(timestamp).date())
        sheet_day: str = time.strftime("%A", time.localtime(timestamp))

        sheet_date_element: typing.Any = self.pdf_serializer.left_align_text(
                f'Date: {sheet_date}')
        sheet_day_element: typing.Any = self.pdf_serializer.right_align_text(
                f'Day: {sheet_day}')

        page_header_table = (self.pdf_serializer.
                generate_table_without_cell_constraints(
                    [[sheet_date_element, sheet_day_element]],
                    False,
                )
            )

        data_table = self.pdf_serializer.generate_table_with_cell_constraints(rows, True)

        self.elements.append(page_header_table)
        self.elements.append(data_table)
        self.elements.append(self.pdf_serializer.get_page_break())


    def build_pdf(self):
        self.doc.build(self.elements)

    def generate(self, cycle: models.Programme):
        self.pdf_serializer.init_pdf('test.pdf')
        self.generate_first_page(cycle)

        key_ordering: typing.List[str] = [
                    'exercise',
                    'equipment',
                    'mass',
                    'set_count',
                    'set_duration',
                    'reps_per_set',
                    'rest_duration',
                    'work_capacity',
                ]

        timestamps: typing.List[int] = list()
        for ts in cycle.sessions.keys():
            timestamps.append(int(ts))

        timestamps.sort()

        for ts in timestamps:
            rows: typing.List[typing.List[typing.Any]] = [
                    self.get_page_headers(),
                ]
            exercises: typing.Dict = cycle.sessions[ts]
            for e in exercises.values():
                row: typing.List[typing.Any] = list()
                for k in key_ordering:
                    val: typing.Any = getattr(e, k)
                    if val is None:
                        val = '-'
                    row.append(val)
                rows.append(row)

            self.prepare_page(ts, rows)

        pdf_saved: bool = self.pdf_serializer.build_pdf(self.elements)
        if pdf_saved:
            print(f'pdf saved to location {self.pdf_serializer.doc.filename}')
