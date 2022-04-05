import typing
from dataclasses import dataclass

@dataclass
class ConfigConstantsClass:
    default_data_dir: str
    default_output_dir: str


ConfigConstants = ConfigConstantsClass(
            default_data_dir="data/",
            default_output_dir="generated/",
        )
