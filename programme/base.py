import abc
import typing

from generators.base import CycleGenerator

class Base:
    @abc.abstractclassmethod
    def validate_starting_conditions(self):
        pass



class ProgrammeGenerator(Base):
    def __init__(self, conditions: typing.Dict,
            volume_cycle_generator: CycleGenerator):
        self.conditions = conditions
        self.volume_cycle_generator = volume_cycle_generator

    def validate_starting_conditions(self):
        return True
