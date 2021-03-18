from Solution.lib import UsecaseBase, AuthBase
from .util import Singleton
from .input import UserInput
from collections import defaultdict
import uuid

class Usecases(metaclass=Singleton):
    def __init__(self):
        self.users = defaultdict(set)
        self.uuids = dict()
        self.usecases = UsecaseBase.get_usecases()
        print('usecases', self.usecases)
        #auth_cls = AuthBase.get_auth_cls()
        #self.auth = auth_cls()

    def get_usecase(self, usecase, user):
        if usecase not in self.usecases:
            raise Exception("Usecase %s is not registered. "\
                    "Available usecases: %s"%(
                        usecase, list(self.usecases.keys())))
        return self.usecases[usecase](user)

    def initialize(self, user, usecases):
        if not usecases:
            return
        for usecase, details in usecases.items():
            for usecase_id, detail in details.items():
                if usecase_id in self.uuids:
                    self.add_user(user, usecase_id)
                    continue
                obj = self.get_usecase(usecase, user)
                obj.initialize(usecase_id=usecase_id, **detail)
#                self.users[user].add(usecase_id)
#                obj.usecase_id = usecase_id
#                self.uuids[usecase_id] = obj

    def register_usecase(self, user, usecase_id, obj):
        self.users[user].add(usecase_id)
        self.uuids[usecase_id] = obj

    def deregister_usecase(self, usecase_id):
        self.uuids.pop(usecase_id, None)

    def dump(self, user):
        usecases = defaultdict(dict)
        for usecase_id in self.users[user]:
            if usecase_id not in self.uuids:
                continue
            obj = self.uuids[usecase_id]
            usecases[obj.__usecase__][usecase_id] = obj.dump()
        return usecases

    def list(self, user, usecase):
        usecases = list()
        for usecase_id in self.users[user]:
            obj = self.uuids[usecase_id]
            if obj.__usecase__ == usecase:
                usecases.append(obj)
        return usecases

    def create(self, user, usecase, *args, **kwargs):
        obj = self.get_usecase(usecase)
        obj.create(*args, **kwargs)
        obj.usecase_id = str(uuid.uuid4())
        self.users[user].add(obj.usecase_id)
        self.uuids[obj.usecase_id] = obj
        return obj

    def delete(self, usecase_id):
        usecase = self.uuids[usecase_id]
        usecase.delete()
        self.uuids.pop(usecase_id)
        for user, uuids in self.users.items():
            if usecase_id in uuids:
                self.users[user].remove(usecase_id)

    def set_default_user(self, user):
        self.default_user = user
        username, password, project = UserInput().get_user_details(user)
        self.auth_h = self.auth.get_auth_h(username, password, project)

    def add_user(self, user, usecase_id):
        self.users[user].add(usecase_id)
