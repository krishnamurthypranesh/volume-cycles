import abc
import typing

from generators import BaseCycleGenerator
from serializers import JsonSerializer, CsvSerializer

class Base:
    @abc.abstractclassmethod
    def validate_starting_conditions(self):
        pass



class ProgrammeGenerator(Base):
    def __init__(self, serializer: JsonSerializer, config_file: str,
            generator: BaseCycleGenerator):
        self.cycle_generator = generator
        self.serializer = serializer
        self.exercises = self.serializer.unmarshal(config_file)


    def validate_starting_conditions(self):
        return True

    def generate_cycle(self):
        return self.cycle_generator.generate(self.exercises)
