import pytest
from Solution.CEM.usecases.demo_usecase import Demo
from Solution.lib.usecases import Usecases
from Solution.lib.session import PyTestSession
from Solution.lib.input import UserInput

class TestDemo(object):
    @classmethod
    def setup_class(cls):
        cls.user = PyTestSession().name
        cls.usecase_args = UserInput().get_usecases(cls.user).get(Demo.__usecase__)
        if not cls.usecase_args:
            pytest.skip("Feature Demo not enabled")
        cls.instances = Usecases().list(cls.user, Demo.__usecase__)

    @pytest.mark.execute
    def test_create_endpoints(self):
        print('Running create scenario in Org')

    @pytest.mark.execute
    def test_update_endpoints(self):
        print('Running update scenario in Org')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_endpoints(self):
        print('Deleting endpoints under %s'%self.user)
