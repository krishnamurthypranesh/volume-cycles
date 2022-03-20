import typing

from models.base import Base

class Exercise(Base):
    def __init__(self, name: str, equipment: str, unilateral: bool,
            exc_type: str):
        self.name = name
        self.equipment = equipment
        self.unilateral = unilateral
        self.exercise_type = exc_type
