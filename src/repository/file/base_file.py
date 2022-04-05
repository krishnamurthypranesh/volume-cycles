import typing
from abc import abstractclassmethod, abstractproperty

class BaseFileRepo(type):
    def __new__(cls, name, bases, body):
        if not 'read' in body:
            raise TypeError('Derived class must implement method: read!')

        if not 'write' in body:
            raise TypeError('Derived class must implement method: write!')

        instance = super(BaseFileRepo, cls).__new__(cls, name, bases, body)
        return instance

    @abstractclassmethod
    def read(self, *args, **kwargs):
        pass

    @abstractclassmethod
    def write(self, *args, **kwargs):
        pass
