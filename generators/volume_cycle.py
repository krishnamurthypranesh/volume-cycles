import time
import typing
import logging
from datetime import datetime

import models
from generators.base import BaseCycleGenerator

class VolumeCycleGenerator(metaclass=BaseCycleGenerator):
    def __init__(self, serializer: typing.Any, logger: logging.Logger):
        self.serializer = serializer
        self.logger = logger
        self.sessions: typing.List[typing.Dict] = list()


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
            ex_session: models.ExerciseSession) -> bool:
        sessions: typing.List[typing.Dict] = self.sessions
        if len(sessions) > 0:
            last: typing.Dict = sessions[-1]

            if last.timestamp == ex_session.timestamp:
                if last.name == ex_session.name:
                    raise Exception('Session already exists!')

                last.exercises[ex_session.exercise] = ex_session
                sessions[-1] = last

            if last.timestamp < ex_session.timestamp:
                session: typing.Dict = models.Session(
                        timestamp=ex_session.timestamp,
                        exerciseSessions={ex_session.exercise: ex_session,},
                )
                sessions.append(session)

            if last.timestamp > ex_session.timestamp:
                raise Exception('Time supplied is already accounted for!')
        else:
            session: models.Session = models.Session(
                        timestamp=ex_session.timestamp,
                        exerciseSessions={ex_session.exercise: ex_session,}
                    )
            sessions.append(session)

        self.sessions = sessions

        return True


    def generate(self, exercises: typing.List[models.Exercise]):
        for exercise in exercises:
            increment: int = exercise.increment_period
            end_epoch: int = exercise.end_timestamp

            epoch: int = exercise.start_timestamp

            while epoch < end_epoch:
                day: str = time.strftime('%A', time.localtime(epoch))

                if exercise.days.get(day):
                    set_count: int = self._calculate_set_count(exercise)
                    session: models.ExerciseSession = models.ExerciseSession(
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
