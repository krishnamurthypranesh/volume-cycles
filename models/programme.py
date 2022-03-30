import time
from datetime import datetime
import typing

from models import Base, Exercise

class Programme(Base):
    def __init__(self, start_date: str, end_date: str,
            exercises: typing.List[Exercise]):
        self.exercises = exercises

    @property
    def start_timestamp(self):
        return self._start_timestamp

    @property
    def end_timestamp(self):
        return self._end_timestamp

    @start_timestamp.setter
    def start_timestamp(self, date: str):
        value = int(datetime.fromtimestamp(
                    time.mktime(
                            time.strptime(date, '%Y-%m-%d')
                        )
                ).timestamp())
        self._start_timestamp = value

    @end_timestamp.setter
    def end_timestamp(self, date: str):
        value = int(datetime.fromtimestamp(
                    time.mktime(
                            time.strptime(date, '%Y-%m-%d')
                        )
                ).timestamp())
        self._end_timestamp = value
