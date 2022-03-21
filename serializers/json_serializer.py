import json
import typing
import logging

from models import Exercise
from serializers.base import Serializer

class JsonSerializer(Serializer):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _read(self, path: str) -> typing.Dict:
        content: typing.Dict = dict()
        try:
            with open(path, 'r') as f:
                content: typing.Dict = json.load(f)
        except Exception as e:
            self.logger.error(e)

        return content

    def _write(self, content: typing.Dict, path: str):
        try:
            with open(path, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            self.logger.error(e)

    def unmarshal(self, path: str):
        exercises: typing.List[Exercise] = list()
        content: typing.Dict = self._read(path)

        for k, v in content.items():
            d: typing.Dict = {**{'name': k}, **v}
            exercise = Exercise(**d)
            exercises.append(exercise)

        return exercises
