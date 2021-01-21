import pytest
from Solution.CEM.usecases.demo_usecase import Demo
from Solution.lib.usecases import Usecases
from Solution.lib.session import PyTestSession
from Solution.lib.input import UserInput

class TestDemo(object):
    @classmethod
    def setup_class(cls):
        cls.user = PyTestSession().name
        cls.children = set()
        for child in UserInput().get_children(cls.user):
            if Demo.__usecase__ in UserInput().get_usecases(child).keys():
                cls.children.add(child)
        if not cls.children:
            pytest.skip("Feature Demo not enabled")

    @pytest.mark.onboard
    def test_onboard_service_provider(self):
        for child in self.children:
            print('Onboarding service provider %s'%child)

    @pytest.mark.execute
    def test_create_user(self):
        print('Running create scenario in SaaS')

    @pytest.mark.execute
    def test_delete_user(self):
        print('Running delete scenario in SaaS')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_service_provider(self):
        for child in self.children:
            print('Deleting service provider %s'%child)
