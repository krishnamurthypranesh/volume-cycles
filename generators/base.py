import abc
import typing

class CycleGenerator:
    @abc.abstractclassmethod
    def generate(self):
        pass
