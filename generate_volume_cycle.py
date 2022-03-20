import csv
import pdb
import json
import time
import typing
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Constants:
    start_timestamp: datetime
    end_timestamp: datetime
    starting_volume: int
    kettlebell_mass_in_kg: int

def init_constants() -> Constants:
    return Constants(
            start_timestamp=datetime(2022,3,21),
            end_timestamp=datetime(2022,4,17),
            starting_volume=3,
            kettlebell_mass_in_kg=14,
    )


EXERCISES: typing.Dict = {
        'Clean and Press': {
            'equipment': 'Kettlebell',
            'unilateral': True,
            'type': 'Strength',
            'reps_per_set': 6,
            'rest_duration': 60,
            'set_duration': None,
        },
        'Deck Squats': {
            'equipment': 'Kettlebell',
            'unilateral': True,
            'type': 'Strength',
            'reps_per_set': 8,
            'rest_duration': 60,
            'set_duration': None,
        },

        'Turkish Get-Ups': {
            'equipment': 'Kettlebell',
            'unilateral': True,
            'type': 'Strength',
            'reps_per_set': 2,
            'rest_duration': 60,
            'set_duration': None,
        },
        'Two Hand Swings': {
            'equipment': 'Kettlebell',
            'unilateral': False,
            'type': 'Strength Endurance',
            'reps_per_set': 5,
            'rest_duration': None,
            'set_duration': 60,
        },
        'Bodyweight - Hindu Push-Ups': {
            'equipment': None,
            'unilateral': False,
            'type': 'Strength Endurance',
            'reps_per_set': 6,
            'rest_duration':None,
            'set_duration': 60,
        },
        'Bodyweight - Cossack Squats': {
            'equipment': None,
            'unilateral': True,
            'type': 'Strength Endurance',
            'reps_per_set': 10,
            'rest_duration':None,
            'set_duration': 60,
        },
        'Bodyweight - Pull-Ups': {
            'equipment': None,
            'unilateral': False,
            'type': 'Strength Endurance',
            'reps_per_set': 4,
            'rest_duration':None,
            'set_duration': 60,
        },
    }

DAYS_EXERCISES: typing.Dict = {
            'Monday': ['Clean and Press', 'Deck Squats'],
            'Tuesday': ['Two Hand Swings', 'Turkish Get-Ups'],
            'Wednesday': [],
            'Thursday': ['Clean and Press', 'Deck Squats'],
            'Friday': ['Two Hand Swings', 'Turkish Get-Ups',
                'Bodyweight - Hindu Push-Ups'],
            'Saturday': ['Bodyweight - Cossack Squats', 'Bodyweight - Pull-Ups'],
            'Sunday': []
        }

EXERCISE_INCREMENT_FREQUENCIES: typing.Dict = {
            'Clean and Press': 2,
            'Deck Squats': 2,
            'Two Hand Swings': 2,
            'Turkish Get-Ups': 2,
            'Bodyweight - Hindu Push-Ups': 1,
            'Bodyweight - Cossack Squats': 1,
            'Bodyweight - Pull-Ups': 1,
        }

SESSIONS: typing.List = []

def get_prev_session_values(exc: str, epoch: int) -> typing.Dict:
    return SESSIONS[-1][exc]


def add_exercise_session_details(exc_session: typing.Dict, epoch: int):
    name: str = exc_session['exercise']
    date: str = str(datetime.fromtimestamp(epoch))

    if len(SESSIONS) > 0:
        last = SESSIONS[-1]

        if last['timestamp'] == epoch:
            if last['exercises'].get(name):
                raise Exception('Session already exists!')

            last['exercises'][name] = exc_session
            SESSIONS[-1] = last

        if last['timestamp'] < epoch:
            latest = {
                'timestamp': epoch,
                'day': time.strftime('%A', time.localtime(epoch)),
                'date': str(datetime.fromtimestamp(epoch)),
                'exercises': {
                    name: exc_session,
                },
            }
            SESSIONS.append(latest)

        if last['timestamp'] > epoch:
            raise Exception('Time supplied is already accounted for!')

    else:
         latest = {
             'timestamp': epoch,
             'day': time.strftime('%A', time.localtime(epoch)),
             'date': str(datetime.fromtimestamp(epoch)),
             'exercises': {
                 name: exc_session,
             },
         }
         SESSIONS.append(latest)


def calculate_set_count(exc):
    cursor_count: int = 0
    last_n_sets: typing.List[int] = list()

    retval:int = 3
    idx: int = len(SESSIONS) - 1

    increment_freq: int = EXERCISE_INCREMENT_FREQUENCIES[exc]

    while idx >= 0:
        if cursor_count >= increment_freq:
            break

        session: typing.Dict = SESSIONS[idx]
        if session['exercises'].get(exc):
            cursor_count += 1
            set_count: int = session['exercises'][exc]['sets']
            last_n_sets.append(set_count)

        idx -= 1

    if len(last_n_sets) >= increment_freq:
        if len(last_n_sets) >= increment_freq:
            # if the set counts are the same, then the sum of the last two sets
            # should be equal to twice any of the set counts
            if sum(last_n_sets) == 2*last_n_sets[0]:
                retval = last_n_sets[0] + 1
            else:
                # the latest set count is inserted first into this list
                # so setting retval to last_n_sets[0]
                retval = last_n_sets[0]

    return retval


def save_json():
    with open('programme.json', 'w') as f:
        json.dump(SESSIONS, f)


def serialize_session_data():
    HEADER: typing.List[str] = ['Sl No', 'Date', 'Day', 'Exercise',
            'Equipment', 'Mass', 'Sets', 'Set Duration(s)', 'Reps/Set',
            'Is Exercise Unilateral?', 'Rest Duration(s)', 'Work Capacity']
    with open('programme.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        counter: int = 1
        for session in SESSIONS:
            try:
                for k, exc in session['exercises'].items():
                    date: str = exc['date'].split(' ')[0]
                    exc_info: typing.Dict = EXERCISES[k]
                    row = [
                            counter,
                            date,
                            exc['day'],
                            exc['exercise'],
                            exc['equipment'],
                            exc['mass in kg'],
                            exc['sets'],
                            exc['set_duration'] or '-',
                            exc['reps_per_set'],
                            exc_info['unilateral'],
                            exc['rest_duration'],
                            exc['work_capacity'],
                        ]
                    writer.writerow(row)
                    counter += 1
            except Exception as e:
                pdb.set_trace()
                print(f'[SERIALIZE SESSION DATA]: {e}')


def main():
    const: Constants = init_constants()
    increment: int = 86400
    epoch: int = int(const.start_timestamp.timestamp())

    while epoch < int(const.end_timestamp.timestamp()):
        day: str = time.strftime('%A', time.localtime(epoch))
        exercises: typing.List[typing.Dict] = DAYS_EXERCISES[day]

        for exc in exercises:
            exc_info: typing.Dict = EXERCISES[exc]

            set_count: int = calculate_set_count(exc)

            curr_session = {
                        'exercise': exc,
                        'day': day,
                        'date': str(datetime.fromtimestamp(epoch)),
                        'equipment': exc_info['equipment'],
                        'mass in kg': const.kettlebell_mass_in_kg,
                        'sets': set_count,
                        'reps_per_set': exc_info['reps_per_set'],
                        'set_duration': exc_info['set_duration'],
                        'rest_duration': exc_info['rest_duration'],
                        'work_capacity': 0,
                    }
            try:
                add_exercise_session_details(curr_session, epoch)
            except Exception as e:
                print(f'[ADD NEW SESSION]: {e}')

        epoch += increment
    save_json()
    serialize_session_data()

if __name__ == '__main__':
    main()
