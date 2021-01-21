import pytest
from Solution.CEM.usecases.vEPC_usecase import Demo2
from Solution.lib.usecases import Usecases
from Solution.lib.session import PyTestSession
from Solution.lib.input import UserInput

class TestvEPC(object):
    @classmethod
    def setup_class(cls):
        '''
        Check if the usecase is enabled in user input and skip the tests if not
        '''
        cls.user = PyTestSession().name
        cls.children = set()
        for child in UserInput().get_children(cls.user):
            if Demo2.__usecase__ in UserInput().get_usecases(child).keys():
                cls.children.add(child)
        if not cls.children:
            pytest.skip("Feature %s not enabled"%Demo2.__usecase__)

    @pytest.mark.onboard
    def test_onboard_service_provider(self):
        '''
        Create Service Provider tenants
        '''
        for child in self.children:
            print('Onboarding service provider %s'%child)

    @pytest.mark.execute
    def test_add_compute(self):
        print('Running create scenario in SaaS')

    @pytest.mark.execute
    def test_delete_user(self):
        print('Running delete scenario in SaaS')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_service_provider(self):
        '''
        Delete Service Provider tenants
        '''
        for child in self.children:
            print('Deleting service provider %s'%child)
