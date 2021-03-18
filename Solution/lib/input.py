from .util import Singleton
import yaml

class UserInput(metaclass=Singleton):
    def __init__(self, inputfile):
        self.users = dict()
        self.parse(inputfile)

    def add_user(self, name, info, role):
        usecase = self.parse_usecase(info.get('usecases'))
        self.users[name] = info
        self.users[name].update({
            'project': info.get('project') or name,
            'children': set(),
            'role': role,
            'usecase': usecase})

    def parse_usecase(self, usecasefile):
        if not usecasefile:
            return dict()
        with open(usecasefile, 'r') as fd:
            parsed = yaml.load(fd, Loader=yaml.FullLoader)
        return parsed or dict()

    def parse(self, inputfile):
        with open(inputfile, 'r') as fd:
            self.parsed = yaml.load(fd, Loader=yaml.FullLoader)
        self.users['saas'] = {
                'username': self.parsed['saas_username'],
                'password': self.parsed['saas_password'],
                'project': self.parsed.get('saas_project'),
                'children': set(),
                'role': 'saas'}
        for sp, sp_info in self.parsed.get('ServiceProviders', dict()).items():
            self.add_user(sp, sp_info, 'service_provider')
            self.users['saas']['children'].add(sp)
            for org, org_info in sp_info.get('Organizations', dict()).items():
                self.add_user(org, org_info, 'organization')
                self.users[sp]['children'].add(org)
                for dept, dept_info in org_info.get('Departments', dict()).items():
                    self.add_user(dept, dept_info, 'department')
                    self.users[org]['children'].add(dept)

    def get_role(self, name):
        return self.users[name]['role']

    def get_children(self, name):
        return list(self.users[name].get('children') or [])

    def get_user_details(self, name):
        if name not in self.users:
            raise Exception('User %s is not registered. Available: %s'%(
                name, list(self.users.keys())))
        details = self.users[name]
        return details['username'], details['password'], details['project']

    def get_usecases(self, name):
        if name not in self.users:
            raise Exception('User %s is not registered. Available: %s'%(
                name, list(self.users.keys())))
        return self.users[name]['usecase']
