import uuid
from Solution.lib import UsecaseBase, AuthBase
from .usecases import Usecases

class Usecase(UsecaseBase):
    def __init__(self, user):
        self.user = user
        self.auth_h = self.get_auth_h(user)
        self.usecase_id = None

    def get_auth_h(self, user):
        auth_cls = AuthBase.get_auth_cls()
        self.auth = auth_cls(user)
        return self.auth

    def initialize(self, usecase_id):
        self.usecase_id = usecase_id
        Usecases().register_usecase(self.user, usecase_id, self)

    def create(self, user=None):
        user = user or self.user
        self.usecase_id = self.usecase_id or str(uuid.uuid4())
        Usecases().register_usecase(user, self.usecase_id, self)

    def delete(self):
        Usecases().deregister_usecase(self.usecase_id)

    def validate(self):
        pass
