import csv
import json
import typing
import logging

from models import Exercise
from repository import file


class ExerciseRepo(metaclass=file.FileBaseRepo):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def marshal(self, *args, **kwargs):
        pass

    def unmarshal(self, *args, **kwargs):
        pass

    def read(self, pth: str):
        exercise: Exercise = None
        ext: str = pth.split('.')[-1]

        with open(pth, 'r') as f:
            data: typing.Dict = json.load(f)
            exercise = Exercise(**data)

        return exercise

    def write(self, pth: str):
        ext: str = pth.split('.')[-1]
        data: typing.Dict = {k:v 
                for k, v in self.__dict__.items() 
                if not k.startswith('__')}
        with open(pth, 'w') as f:
            for

