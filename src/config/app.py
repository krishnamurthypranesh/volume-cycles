import os

from dataclasses import dataclass

from constants.configuration import ConfigConstants

@dataclass
class _AppConfigClass:
    DATA_DIR: str
    OUTPUT_DIR: str

AppConfig = _AppConfigClass(
            DATA_DIR=os.environ.get('VOLUME_CYCLE_DATA_DIR',
                    ConfigConstants.default_data_dir,
                ),
            OUTPUT_DIR=os.environ.get('VOLUME_CYCLE_OUTPUT_DIR',
                    ConfigConstants.default_output_dir,
                )

        )
