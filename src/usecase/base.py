import abc
import typing

class BaseUseCase(type):
    def __new__(cls, name, bases, body):
        if not 'generate' in body:
            raise TypeError("Derived class must implement method: generate!")

        return super().__new__(cls, name, bases, body)

    @abc.abstractclassmethod
    def generate(self):
        pass
