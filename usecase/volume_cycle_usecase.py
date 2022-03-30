import time
import typing
import logging
from datetime import datetime

import models
from models import inputs
from usecase.base import BaseUseCase
from constants import CommonConstants

class InvalidInitConditionsException(Exception):
    pass

class ConflictingScheduleException(Exception):
    pass

class VolumeCycleGeneratorUseCase(metaclass=BaseUseCase):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.sessions: typing.Dict = dict()


    def _calculate_set_count(self, exercise: inputs.ExerciseInput, curr: int,
            prev: typing.List[int]) -> int:
        res: int = exercise.starting_set_count
        set_counts: typing.List[int] = []

        for pe in prev:
            if self.sessions.get(pe):
                session = self.sessions[pe]
                if session.get(exercise.name):
                    set_counts.append(session[exercise.name].set_count)

        if len(set_counts) <= 1:
            res = exercise.starting_set_count
        elif len(set_counts) > 1:
            avg_set_count: int = int(sum(set_counts)/len(set_counts))
            if avg_set_count == set_counts[0]:
                res = avg_set_count + exercise.increment_step
            else:
                res = set_counts[-1]

        return res


    def _add_exercise_session_details(self,
            ex_session: models.Session) -> bool:
        if self.sessions.get(ex_session.timestamp):

            if self.sessions.get(ex_session, {}).get(ex_session.exercise):
                raise ConflictingScheduleException(f'Exercise {ex_session.name} '
                    'already exists on this date!')

            self.sessions[ex_session.timestamp].update(
                    {ex_session.exercise: ex_session},
                )

        else:
            self.sessions[ex_session.timestamp] = {
                        ex_session.exercise: ex_session,
                    }

        return True


    def _validate_init_conditions(self,
            init_conditions: inputs.VolumeCycleInitConditions) -> bool:
        conditions: typing.List[bool] = [
                    (init_conditions.end_timestamp >=
                    init_conditions.start_timestamp),
                ]

        return all(conditions)


    def _get_exercise_schedule(self, start_epoch: int, end_epoch: int,
            days: typing.Dict) -> typing.List[int]:
        epochs: typing.List[int] = list()

        prev_epoch: int = 0
        curr_epoch: int = start_epoch

        while curr_epoch < end_epoch:
            day: str = time.strftime('%A', time.localtime(curr_epoch))
            if days.get(day):
                epochs.append(curr_epoch)

            prev_epoch = curr_epoch
            curr_epoch += CommonConstants.seconds_in_a_day
        return epochs


    def generate(self, init_conditions: inputs.VolumeCycleInitConditions):
        if not self._validate_init_conditions(init_conditions):
            return InvalidInitConditionsException(
            'Invalid starting conditions provided!')

        for exercise in init_conditions.exercises_input:
            epoch: int = init_conditions.start_timestamp

            epochs: typing.List[int] = self._get_exercise_schedule(
                        init_conditions.start_timestamp,
                        init_conditions.end_timestamp,
                        exercise.days,
                    )

            for idx in range(len(epochs)):
                curr_epoch: int = epochs[idx]

                start: int = max([0, idx - exercise.increment_frequency])
                end: int = max([0, idx])

                prev_epochs: typing.List[int] = epochs[start:end]

                set_count: int = self._calculate_set_count(exercise, epoch,
                        prev_epochs)
                session: models.Session = models.Session(
                            exercise=exercise.name,
                            timestamp=curr_epoch,
                            equipment=exercise.equipment,
                            mass=exercise.mass,
                            set_count=set_count,
                            reps_per_set=exercise.reps_per_set,
                            set_duration=exercise.set_duration,
                            rest_duration=exercise.rest_duration,
                        )
                self._add_exercise_session_details(session)

        return self.sessions
