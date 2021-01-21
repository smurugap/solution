import pytest
import random
from Solution.CEM.usecases.demo_usecase import Demo
from Solution.lib.usecases import Usecases
from Solution.lib.session import PyTestSession
from Solution.lib.input import UserInput

class TestDemo(object):
    @classmethod
    def setup_class(cls):
        cls.user = PyTestSession().name
        cls.usecase_args = UserInput().get_usecases(cls.user).get(Demo.__usecase__)
        if not cls.usecase_args or not cls.usecase_args.get('count'):
            pytest.skip("Feature Demo not enabled")

        cls.children = list()
        for child in UserInput().get_children(cls.user):
            if Demo.__usecase__ in UserInput().get_usecases(child).keys():
                cls.children.append(child)
        if not cls.children:
            pytest.skip("Feature Demo not enabled on any one of the organizations")

        cls.instances = Usecases().list(cls.user, Demo.__usecase__)

    @pytest.mark.onboard
    def test_onboard_organization(self):
        for child in self.children:
            print('Onboarding organization %s'%child)

    @pytest.mark.onboard
    def test_create_usecase(self):
        for i in range(0, self.usecase_args.get('count')):
            obj = Demo(self.user)
            obj.create('vn_%s'%i, ['vm_%s'%i, 'vm_%s'%(i*2 + 1)])
            organization = self.children[i%len(self.children)]
            Usecases().add_user(organization, obj.usecase_id)
            print('created a usecase and shared with org %s'%organization)

    @pytest.mark.execute
    def test_delete_and_recreate_usecase(self):
        instance = random.choice(self.instances)
        instance.delete()
        instance.create('vn-recreated', ['vm-recreated'])
        print('Executed delete and recreate scenario of usecase id %s'%instance.usecase_id)

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_organization(self):
        for instance in self.instances:
            instance.delete()
        for child in self.children:
            print('Deleted organization account %s'%child)
