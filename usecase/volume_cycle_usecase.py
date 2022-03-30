import time
import typing
import logging
from datetime import datetime

import models
from models import inputs
from usecase.base import BaseUseCase

class InvalidInitConditionsException(Exception):
    pass

class ConflictingScheduleException(Exception):
    pass

class VolumeCycleGeneratorUseCase(metaclass=BaseUseCase):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.sessions: typing.Dict = dict()


    def _calculate_set_count(self, exercise: str) -> int:
        cursor_count: int = 0
        last_n_sets: typing.List[int] = list()

        retval: int = exercise.starting_set_count
        idx: int = len(self.sessions) - 1

        increment_frequency: int = exercise.increment_frequency

        while idx >= 0:
            if cursor_count >= increment_frequency:
                break

            session: models.Session = self.sessions[idx]
            if session.exercises.get(exercise.name):
                cursor_count += 1
                set_count: int = session.exercises[exercise.name].set_count
                last_n_sets.append(set_count)

            idx -= 1

        if len(last_n_sets) >= increment_frequency:
            if len(last_n_sets) >= increment_frequency:
                if sum(last_n_sets) == 2 * last_n_sets[0]:
                    retval = last_n_sets[0] + exercise.increment_step
                else:
                    retval = last_n_sets[0]

        return retval


    def _add_exercise_session_details(self,
            ex_session: models.Session) -> bool:
        if self.sessions.get(ex_session.timestamp):
            if self.sessions.get(ex_session, {}).get(ex_session.name):
                raise ConflictingScheduleException(f'Exercise {ex_session.name} '
                    'already exists on this date!')

            self.sessions[ex_session.name] = ex_session

        else:
            self.sessions[ex_session.timestamp] = {
                        ex_session.name: ex_session,
                    }

        return True


    def _validate_init_conditions(self,
            init_conditions: inputs.VolumeCycleInitConditions) -> bool:
        conditions: typing.List[bool] = [
                    (init_conditions.end_timestamp >=
                    init_conditions.start_timestamp),
                ]

        return all(conditions)


    def generate(self, init_conditions: inputs.VolumeCycleInitConditions):
        if not self._validate_init_conditions(init_conditions):
            return InvalidInitConditionsException(
            'Invalid starting conditions provided!')

        for exercise in init_conditions.exercises_input:
            increment: int = exercise.increment_period
            end_epoch: int = init_conditions.end_timestamp

            epoch: int = init_conditions.start_timestamp

            while epoch < end_epoch:
                day: str = time.strftime('%A', time.localtime(epoch))

                if exercise.days.get(day):
                    set_count: int = self._calculate_set_count(exercise)
                    session: models.Session = models.Session(
                                exercise=exercise.name,
                                timestamp=epoch,
                                equipment=exercise.equipment,
                                mass=exercise.mass,
                                set_count=set_count,
                                reps_per_set=exercise.reps_per_set,
                                set_duration=exercise.set_duration,
                                rest_duration=exercise.rest_duration,
                            )
                    self._add_exercise_session_details(session)
                epoch += increment

        return self.sessions
