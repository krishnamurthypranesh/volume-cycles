import time
import typing
from datetime import datetime

from models import Base, Exercise, Session

class Programme(Base):
    def __init__(self, start_timestamp: int,
            end_timestamp: int,
            exercises: typing.List[Exercise],
            sessions: typing.List[Session]):
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self.exercises = exercises
        self.sessions = sessions

    @property
    def start_timestamp(self):
        return self._start_timestamp

    @property
    def end_timestamp(self):
        return self._end_timestamp

    @start_timestamp.setter
    def start_timestamp(self, ts: int):
        self._start_timestamp = ts 

    @end_timestamp.setter
    def end_timestamp(self, ts: int):
        self._end_timestamp = ts

    def get_start_date(self):
        date = datetime.fromtimestamp(self.start_timestamp)
        return str(date.date())

    def get_end_date(self):
        date = datetime.fromtimestamp(self.end_timestamp)
        return str(date.date())
