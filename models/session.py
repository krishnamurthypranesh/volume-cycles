import typing

from base import Base
from models.exercise import Exercise


class Session(Base):
    def __init__(self, exercises: typing.List[Exercise]):
        self.exercises = exercises
