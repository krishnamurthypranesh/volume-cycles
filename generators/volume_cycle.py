import typing
import logging

import models
from generators.base import CycleGenerator

class VolumeCycleGenerator(CycleGenerator):
    def __init__(self, exercises: typing.List[models.Exercise],
            serializer: typing.Any, logger: logging.Logger):
        self.exercises = exercises
        self.serializer = serializer
        self.logger = logger
        self.sessions: typing.List[models.Session] = list()


    def _calculate_set_count(self, exercise: str) -> int:
        cursor_count: int = 0
        last_n_sets: typing.List[int] = list()

        retval: int = exercise.starting_conditions.set_count
        idx: int = len(self.sessions) - 1

        increment_frequency: int = exercise.increment_frequency

        while idx >= 0:
            if cursor_count >= increment_frequency:
                break

            session: models.Session = self.sessions[idx]
            if session.exercises.get([exercise.name]):
                cursor_count += 1
                set_count: int = session.exercises[exercise.name].set_count
                last_n_sets.append(set_count)

            idx -= 1

        if len(last_n_sets) >= increment_frequency:
            if len(last_n_sets) >= increment_frequency:
                if sum(last_n_sets) == 2 * last_n_sets[0]:
                    retval = last_n_sets[0] + 1
                else:
                    retval = last_n_sets[0]

        return retval


    def _add_exercise_session_details(self, ex_session: models.ExerciseSession) -> bool:
        sessions: typing.List[models.Session] = self.sessions

        if len(sessions) > 0:
            last: models.Session = sessions[-1]

            if last.timestamp == ex_session.timestamp:
                if last.name == ex_session.name:
                    raise Exception('Session already exists!')

                last.exercises[ex_session.exercise] = ex_session
                sessions[-1] = last

                if last.timestamp < ex_session.timestamp:
                    session: models.Session = models.Session(
                            timestamp=session.timestamp,
                            exercises={ex_session.exercise: ex_session,},
                    )
                    sessions.append(session)

                if last.timestamp > ex_session.timestamp:
                    raise Exception('Time supplied is already accounted for!')
        else:
            session: models.Session = models.Session(
                        timestamp=ex_session.timestamp,
                        exercises={ex_session.exercise: ex_session,}
                    )
            sessions.append(session)

        self.sessions = sessions

        return True


    def generate(self):
        for exercise in self.exercises:
            increment: int = exercise.starting_conditions.increment_period
            end_epoch: int = int(exercise.starting_conditions.
                    end_timestamp.timestamp())
            epoch: int = int(exercise.starting_conditions.
                    start_timestamp.timestamp())

            while epoch < end_epoch:
                set_count: int = calculate_set_count(exercise)

                session: models.Session = models.ExerciseSession(
                            timestamp
                            exercise=exercise.name,
                            equipment=exercise.equipment,
                            mass=exercise.mass,
                            set_count=set_count,
                            set_duration=exercise.set_duration,
                            reps_per_set=exercise.reps_per_set,
                            rest_duration=exercise.rest_duration,
                        )
                self.add_exercise_session_details(session)
                epoch += increment
