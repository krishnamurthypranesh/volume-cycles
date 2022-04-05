# File to store constants which are common to the app
import typing
from dataclasses import dataclass


@dataclass
class CommonConstantsClass:
    seconds_in_a_day: int
    days_of_the_week: typing.List[str]

CommonConstants = CommonConstantsClass(
            seconds_in_a_day=1*86400,
            days_of_the_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday',],
        )
