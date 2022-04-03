import logging
import argparse

from repository import file as fileRepo
from resource import VolumeCycleProgrammeGeneratorResource
from usecase import VolumeCycleGeneratorUseCase, GenerateCyclePdfUsecase

# test input
filename: str = 'test.json'
programme_type: str = 'volume_cycle'


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    json_serializer = fileRepo.JsonSerializer(logger)
    csv_serializer = fileRepo.CsvSerializer(logger)

    volume_cycle_generator_usecase = VolumeCycleGeneratorUseCase(logger)
    pdf_generator_usecase = GenerateCyclePdfUsecase(logger)

    volume_cycle_programme_generator = VolumeCycleProgrammeGeneratorResource(
            filename,
            csv_serializer,
            json_serializer,
            volume_cycle_generator_usecase,
            pdf_generator_usecase,
    )

    if programme_type == 'volume_cycle':
        value = volume_cycle_programme_generator.generate_cycle()

    print(value)
