"""
- get a cycle
- create an empty canvas
- create the first page
    - add a table listing the exercises performed on each day of the week
    - if a day has no exercises, then mark that as a rest day
- After the first page
- For each timestamp, get the date, day and other bits of information
- For each exercise that needs to be performed on that day, add the session
  details
"""
import time
import uuid
import typing
import logging
from datetime import datetime

from reportlab import platypus
from reportlab.lib import colors, pagesizes, styles, enums

import models
from usecase import BaseUseCase

class GenerateCyclePdfUsecase(metaclass=BaseUseCase):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.elements = []

    def _init_pdf(self):
        #TODO: move folder to constants
        filename: str = f'generated/{uuid.uuid1()}.pdf'
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
        programme_days: typing.Dict = {}
        dex_max: int = 0

        sessions = cycle.sessions

        for k in sessions.keys():
            day: str = time.strftime("%A", time.localtime(int(k)))
            if programme_days.get(day) is not None:
                for e in sessions[k].keys():
                    if not e in programme_days[day]:
                        programme_days[day].append(e)

                        if len(programme_days[day]) > dex_max:
                            dex_max = len(programme_days[day])
            else:
                programme_days[day] = list()

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

        t = platypus.Table(rows,
                colWidths=3*(0.4*pagesizes.inch),
                rowHeights=2*(0.4*pagesizes.inch),
            )

        t.setStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ])

        self.elements.append(t)
        self.elements.append(platypus.PageBreak())


    def prepare_page(self, timestamp: int, rows: typing.List[typing.Any]):
        sheet_date: str = str(datetime.fromtimestamp(timestamp).date())
        sheet_day: str = time.strftime("%A", time.localtime(timestamp))

        _style: typing.Any = styles.ParagraphStyle(
                    name='sheet_date_element',
                    parent=None,
                    alignment=enums.TA_LEFT,
                )
        sheet_date_element: typing.Any = platypus.Paragraph(
                    f'Date: {sheet_date}',
                    style=_style,
                )

        _style: typing.Any = styles.ParagraphStyle(
                    name='sheet_day_element',
                    parent=None,
                    alignment=enums.TA_RIGHT,
                )
        sheet_day_element: typing.Any = platypus.Paragraph(
                    f'Day: {sheet_day}',
                    style=_style,
                )

        page_data = [
                    [sheet_date_element, sheet_day_element,]
                ]
        page_data_table = platypus.Table(
                    page_data,
                )

        _table = platypus.Table(rows,
                colWidths=3*(0.4*pagesizes.inch),
                rowHeights=(2*(0.4*pagesizes.inch)),
            )
        _table.setStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ])

        self.elements.append(page_data_table)
        self.elements.append(_table)
        self.elements.append(platypus.PageBreak())


    def build_pdf(self):
        self.doc.build(self.elements)

    def generate(self, cycle: models.Programme):
        self._init_pdf()
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

        self.build_pdf()
