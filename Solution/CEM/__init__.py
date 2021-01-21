from .usecases import demo_usecase, vEPC_usecase
from Solution.lib import AuthBase

class Auth(AuthBase):
    def __init__(self, user):
        pass

    def get_auth_h(self):
        print("Auth for", username, password, project)
