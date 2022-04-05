import abc
import typing

class BaseResource(type):
    def __new__(cls, name, bases, body):
        if not 'generate_cycle' in body:
            raise TypeError('Derived class must implement method: '
                    'generate_cycle')

        return super().__new__(cls, name, bases, body)

