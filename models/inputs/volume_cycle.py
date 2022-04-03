import time
import typing
from datetime import datetime

class ExerciseInput:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


    @classmethod
    def from_dict(self, _dict: typing.Dict):
        days: typing.Dict = {}
        for day in _dict['days']:
            days[day] = True

        exercise_input = ExerciseInput(
            name=_dict['name'],
            starting_set_count=_dict['starting_set_count'],
            equipment=_dict['equipment'],
            mass=_dict['mass'],
            unilateral=_dict['unilateral'],
            reps_per_set=_dict['reps_per_set'],
            increment_period=_dict['increment_period'],
            increment_frequency=_dict['increment_frequency'],
            increment_step=_dict['increment_step'],
            rest_duration=_dict.get('rest_duration'),
            set_duration=_dict.get('set_duration'),
            days=days,
        )

        return exercise_input

class VolumeCycleInitConditions:
    def __init__(self, programme_start_date: str, programme_end_date: str):
        self.start_timestamp = programme_start_date
        self.end_timestamp = programme_end_date

        self._exercises_input = []

    @property
    def start_timestamp(self) -> int:
        return self._start_timestamp

    @start_timestamp.setter
    def start_timestamp(self, date: str):
        value = int(datetime.fromtimestamp(
                    time.mktime(
                            time.strptime(date, '%Y-%m-%d')
                        )
                ).timestamp())
        self._start_timestamp = value

    @property
    def end_timestamp(self) -> int:
        return self._end_timestamp

    @end_timestamp.setter
    def end_timestamp(self, date: str):
        value = int(datetime.fromtimestamp(
                    time.mktime(
                            time.strptime(date, '%Y-%m-%d')
                        )
                ).timestamp())
        self._end_timestamp = value

    @property
    def exercises_input(self):
        return self._exercises_input

    @exercises_input.setter
    def exercises_input(self, exercises_input: typing.List[ExerciseInput]):
        self._exercises_input = exercises_input



