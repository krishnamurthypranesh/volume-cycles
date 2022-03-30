import typing

from models import inputs
from resource import BaseResource
from usecase import BaseUseCase
from repository import file

# this should get a bunch of the repos
class VolumeCycleProgrammeGeneratorResource(metaclass=BaseResource):
    def __init__(self,
            init_file: str,
            csv_repo: file.BaseFileRepo,
            json_repo: file.BaseFileRepo,
            generator: BaseUseCase):

        self.cycle_generator = generator
        self.init_file = init_file
        self.json_repo = json_repo
        self.csv_repo = csv_repo

    def fetch_init_conditions_from_file(self):
        if self.init_file.endswith('json'):
            self.init_conditions = self.json_repo.read(self.init_file)

        if self.init_file.endswith('csv'):
            self.init_conditions = self.csv_repo.read(self.init_file)

    def generate_cycle(self):
        self.fetch_init_conditions_from_file()

        exercises_input: typing.List[inputs.ExerciseInput] = list()
        ex_inputs = self.init_conditions['exercises']
        for _ex_input in ex_inputs:
            exercises_input.append(inputs.ExerciseInput.from_dict(_ex_input))

        volume_cycle_init_conditions= inputs.VolumeCycleInitConditions(
                self.init_conditions['start_date'],
                self.init_conditions['end_date'],
            )
        volume_cycle_init_conditions.exercises_input = exercises_input

        cycle = self.cycle_generator.generate(volume_cycle_init_conditions)
        import pdb; pdb.set_trace()

        return cycle

