import time
import typing
from datetime import datetime

from models.base import Base


class Session(Base):
    def __init__(self, timestamp: int,
            exerciseSessions: typing.Dict):
        self.exercises = exerciseSessions
        self.timestamp = timestamp

        self.date = timestamp
        self.day = timestamp

    @property
    def date(self):
        return self._date

    @property
    def day(self):
        return self._day

    @date.setter
    def date(self, timestamp: int):
        value = str(datetime.fromtimestamp(timestamp))
        self._date = value

    @day.setter
    def day(self, timestamp: int):
        value = time.strftime('%A', time.localtime(timestamp))
        self._day = value
