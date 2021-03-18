from .input import UserInput
from .artifact import Artifact
from .util import Singleton
import importlib

def dynamic_import(product):
    importlib.import_module("Solution.%s"%product)

class PyTestSession(metaclass=Singleton):
    def __init__(self, artifact=None, user_input=None, execution_id=None, product=None):
        self.artifact = artifact
        self.user_input = user_input
        self.execution_id = execution_id
        dynamic_import(product)

    def initialize(self):
        print('Reading from artifact {} and user_input {}'.format(
            self.artifact, self.user_input))
        UserInput(self.user_input)
        self.name = Artifact(self.artifact).name
        #self.role = Artifact(self.artifact).role
        #self.logger = log.getLogger(self.name, self.execution_id)

    def close(self):
        # Write back the modified dicts to respective json files
        # Should never update Parents artifacts file but can update childrens artifacts
        Artifact().write_back()
