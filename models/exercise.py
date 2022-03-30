import time
import typing
from datetime import datetime

from models.base import Base

class Exercise(Base):
    def __init__(self, name: str, start_date: str, end_date: str,
            starting_set_count: int, equipment: str, mass: int,
            unilateral: bool, reps_per_set: int, rest_duration: int,
            set_duration: int, increment_period: int, increment_frequency: int,
            increment_step: int, days: typing.List[str]):
        self.name = name
        self.starting_set_count = starting_set_count
        self.equipment = equipment
        self.unilateral = unilateral
        self.reps_per_set = reps_per_set
        self.rest_duration = rest_duration
        self.set_duration = set_duration
        self.increment_period = increment_period
        self.increment_frequency = increment_frequency
        self.increment_step = increment_step

        self.days = days
