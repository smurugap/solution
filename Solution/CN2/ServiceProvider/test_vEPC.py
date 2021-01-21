import pytest
import random
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
        cls.usecase_args = UserInput().get_usecases(cls.user).get(Demo2.__usecase__)
        if not cls.usecase_args or not cls.usecase_args.get('count'):
            pytest.skip("Feature %s not enabled"%Demo2.__usecase__)

        '''
        Check if the usecase is enabled in any of the children else skip
        '''
        cls.children = list()
        for child in UserInput().get_children(cls.user):
            if Demo2.__usecase__ in UserInput().get_usecases(child).keys():
                cls.children.append(child)
        if not cls.children:
            pytest.skip("Feature vCPE not enabled on any one of the organizations")

        '''
        During reinvocation get the list of precreated instances of the usecase
        '''
        cls.instances = Usecases().list(cls.user, Demo2.__usecase__)

    @pytest.mark.onboard
    def test_onboard_organization(self):
        for child in self.children:
            print('Onboarding organization %s'%child)

    @pytest.mark.onboard
    def test_create_usecase(self):
        for i in range(0, self.usecase_args.get('count')):
            obj = Demo2(self.user)
            obj.create('si_%s'%i, ['svm_%s'%(i*2), 'svm_%s'%(i*2 + 1)])
            organization = self.children[i%len(self.children)]
            Usecases().add_user(organization, obj.usecase_id)
            print('created a vCPE instance and shared with org %s'%organization)

    @pytest.mark.execute
    def test_delete_and_recreate_usecase(self):
        '''
        Read optional arg from scenario input and act accordingly
        '''
        n_instances = self.usecase_args.get('recreate_instances', 1)
        instances = random.sample(self.instances, n_instances)
        for instance in instances:
            instance.delete()
        for instance in instances:
            instance.create('si-recreated', ['svm-recreated'])
            print('Executed delete and recreate scenario of usecase id %s'%instance.usecase_id)

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_organization(self):
        for instance in self.instances:
            instance.delete()
        for child in self.children:
            print('Deleted organization account %s'%child)
