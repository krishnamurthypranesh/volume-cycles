import json
import typing
import logging

from base import Serializer

class JsonSerializer(Serializer):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def read(self, path: str) -> typing.Dict:
        content: typing.Dict = dict()
        try:
            with open(path, 'r') as f:
                content: typing.Dict = json.load(f)
        except Exception as e:
            self.logger.error(e)

        return content

    def write(self, content: typing.Dict, path: str):
        try:
            with open(path, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            self.logger.error(e)
