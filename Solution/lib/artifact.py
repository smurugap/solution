from .util import Singleton, touch
from .input import UserInput
from .usecases import Usecases
from .flows import Flows
import yaml
import os

class Artifact(metaclass=Singleton):
    def __init__(self, artifact, role=None, name=None):
        #self.role = role or 'SaaS'
        self.name = name or 'saas'
        self.artifacts = dict()
        self.parse(artifact)
        self.children = UserInput().get_children(self.name) or list()
        #Usecases().set_default_user(self.name)
        if self.name == 'saas':
            self.artifacts['saas'] = artifact

    def _parse_children(self, artifact):
        touch(artifact)
        with open(artifact, 'r') as fd:
            parsed = yaml.load(fd, Loader=yaml.FullLoader)
        if not parsed:
            return
        for child in parsed.get('children') or []:
            self._parse_children(child)
        #user_session = self.get_user_handle(self.name)
        self.artifacts[parsed['name']] = artifact
        Usecases().initialize(parsed['name'], parsed.get('usecases'))
        Flows().initialize(parsed.get('flows'))
        return parsed

    def _parse_parent(self, artifact):
        with open(artifact, 'r') as fd:
            parsed = yaml.load(fd, Loader=yaml.FullLoader)
        if not parsed:
            return
        if parsed.get('parent'):
            self._parse_parent(parsed['parent'])
        self.artifacts[parsed['name']] = artifact
        Usecases().initialize(parsed['name'], parsed.get('usecases'))
        Flows().initialize(parsed.get('flows'))

    def parse(self, artifact):
        # Read artifact file
        self.parsed = self._parse_children(artifact)
        #if not self.parsed and self.role == 'SaaS':
        if not self.parsed:
            return
        self.name = self.parsed['name']
        self._parse_parent(artifact)
        #self.role = self.parsed['role']
        #self.parent = self.parsed['parent']

    def write_back(self):
        self.check_and_create_children()
        for name, filename in self.artifacts.items():
            with open(filename, 'r') as fd:
                dct = yaml.load(fd, Loader=yaml.FullLoader) or dict()
            dct['usecases'] = dict(Usecases().dump(name) or {})
            dct['flows'] = dict(Flows().dump(name) or {})
            if name == self.name:
                dct['children'] = [self.artifacts[x] for x in self.children]
                dct['name'] = self.name
            with open(filename, 'w+') as fd:
                yaml.dump(dct, fd)

    def check_and_create_children(self):
        for child in self.children:
            if child not in self.artifacts:
                self.create_child(child)

    def create_child(self, child):
        parent = self.artifacts[self.name]
        filename = os.path.join(os.path.dirname(os.path.abspath(parent)), child+'_artifact.yaml')
        role = UserInput().get_role(child)
        dct = {'parent': parent, 'name': child, 'role': role}
        with open(filename, 'x') as fd:
            yaml.dump(dct, fd)
        self.artifacts[child] = filename
