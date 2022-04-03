import time
import typing
from datetime import datetime

from models.base import Base

class Exercise(Base):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(self, _dict: typing.Dict):
        exercise = Exercise(
            name=_dict['name'],
            starting_set_count=_dict['starting_set_count'],
            equipment=_dict['equipment'],
            unilateral=_dict['unilateral'],
            reps_per_set=_dict['reps_per_set'],
            rest_duration=_dict['rest_duration'],
            set_duration=_dict['set_duration'],
            increment_period=_dict['increment_period'],
            increment_frequency=_dict['increment_frequency'],
            increment_step=_dict['increment_step'],
            days=_dict['days'],
        )

    def __repr__(self):
        rpr = {k:v for k, v in self.__dict__.items() if not k.startswith('__')}
        return f'{rpr}'

    def __str__(self):
        rpr = {k:v for k, v in self.__dict__.items() if not k.startswith('__')}
        return f'{rpr}'
