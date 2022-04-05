import os
import json
import typing
import logging

from models import Exercise
from repository.file import BaseFileRepo

class JsonSerializer(metaclass=BaseFileRepo):
    def __init__(self, logger: logging.Logger,
            data_dir: str, output_dir: str):
        self.logger = logger
        self.data_dir = data_dir
        self.output_dir = output_dir

    def read(self, fname: str) -> typing.Dict:
        content: typing.Dict = dict()
        path: str = os.path.join(self.data_dir, fname)
        try:
            with open(path, 'r') as f:
                content: typing.Dict = json.load(f)
        except Exception as e:
            self.logger.error(e)

        return content

    def write(self, content: typing.Dict, fname: str):
        path: str = os.path.join(self.output_dir, fname)
        try:
            with open(fname, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            self.logger.error(e)
