import typing
from abc import abstractclassmethod, abstractproperty


class Serializer:
    @abstractclassmethod
    def read(self, *args, **kwargs):
        pass

    @abstractclassmethod
    def write(self, *args, **kwargs):
        pass
