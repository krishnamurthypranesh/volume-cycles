# File to store constants which are common to the app
import typing
from dataclasses import dataclass


@dataclass
class CommonConstantsClass:
    seconds_in_a_day: int

CommonConstants = CommonConstantsClass(
            seconds_in_a_day=1*86400,
        )
