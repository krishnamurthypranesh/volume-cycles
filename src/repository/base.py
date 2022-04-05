import typing
from abc import abstractclassmethod, abstractproperty


class BaseRepo(type):
    def __new__(cls, name, bases, body):
        if not 'marshal' in body:
            raise TypeError('Derived class must implement method: marshal')

        if not 'unmarshal' in body:
            raise TypeError('Derived class must implement method: unmarshal')

        return super().__new__(cls, name, bases, body)

    @abstractclassmethod
    def unmarshal(self, *args, **kwargs):
        pass

    @abstractclassmethod
    def marshal(self, *args, **kwargs):
        pass
