import logging
import argparse

from config import AppConfig 
from repository import file as fileRepo
from resource import VolumeCycleProgrammeGeneratorResource
from usecase import VolumeCycleGeneratorUseCase, GenerateCyclePdfUsecase

# test input
filename: str = 'test.json'
programme_type: str = 'volume_cycle'


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    json_serializer = fileRepo.JsonSerializer(
                logger,
                AppConfig.DATA_DIR,
                AppConfig.OUTPUT_DIR,
            )
    csv_serializer = fileRepo.CsvSerializer(logger)
    pdf_serializer = fileRepo.PdfSerializer(logger, AppConfig.OUTPUT_DIR)

    volume_cycle_generator_usecase = VolumeCycleGeneratorUseCase(logger)
    pdf_generator_usecase = GenerateCyclePdfUsecase(
                logger,
                AppConfig.OUTPUT_DIR,
                pdf_serializer,
            )

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
