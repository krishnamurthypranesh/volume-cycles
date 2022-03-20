import csv
import typing
import logging

class CSVSerializer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def read(self, path: str) -> typing.List[typing.Any]:
        rows: typing.List[typing.Any] = list()
        try:
            with open(path, 'r') as f:
                reader = csv.reader(f)
                for idx, row in enumerate(reader):
                    rows.append(row)

                self.logger.info(f'Read {idx + 1} rows')

        except Exception as e:
            self.logger.error(e)

        return rows

    def write(self, path: str, content: typing.List[typing.Any]) -> bool:
        success: bool = False
        try:
            with open(path, 'w') as f:
                writer = csv.writer(f)
                for idx, row in enumerate(content):
                    writer.writerow(row)
                self.logger.info(f'wrote {idx + 1} rows')
                success = True
        except Exception as e:
            self.logger.error(e)

        return success
