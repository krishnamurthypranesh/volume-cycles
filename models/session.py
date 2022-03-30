import time
import typing
import datetime

from models.base import Base

class Session(Base):
    def __init__(self, timestamp: int, exercise: str,
            equipment: str, mass: int, set_count: int,
            set_duration: int, reps_per_set: int,
            rest_duration: int):
        self.timestamp = timestamp
        self.date = datetime.datetime.fromtimestamp(timestamp)
        self.day = time.strftime('%A', time.localtime(timestamp))
        self.exercise = exercise
        self.equipment = equipment
        self.mass = mass
        self.set_count = set_count
        self.set_duration = set_duration
        self.reps_per_set = reps_per_set
        self.rest_duration = rest_duration

        self.calculate_work_capacity()

    def __repr__(self):
        rpr = {k:v for k, v in self.__dict__.items() if not k.startswith('__')}
        return f'{rpr}'

    def __str__(self):
        rpr = {k:v for k, v in self.__dict__.items() if not k.startswith('__')}
        return f'{rpr}'

    def calculate_work_capacity(self):
        self.work_capacity = self.reps_per_set * self.set_count * self.mass
        return self.work_capacity
