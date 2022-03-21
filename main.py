import logging
import argparse

from programme.base import ProgrammeGenerator
from serializers import JsonSerializer, CsvSerializer
from generators import VolumeCycleGenerator

# test input
filename: str = 'test.json'


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    json_serializer = JsonSerializer(logger)
    csv_serializer = CsvSerializer(logger)

    generator = VolumeCycleGenerator(logger, csv_serializer)

    programme_generator = ProgrammeGenerator(
            json_serializer,
            filename,
            generator,
    )

    value = programme_generator.generate_cycle()
    print(value)
