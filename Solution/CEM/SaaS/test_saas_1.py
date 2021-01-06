import pytest
from Tests.Solution.lib import session

class TestAccountManagement(object):
    @classmethod
    def setup_class(cls):
#        logger.info("Inside setup_class")
        print('Inside setup_class')

    @pytest.mark.onboard
    def test_onboard_service_provider(self):
        print('onboarded SP')
#        IntraVN()
#        uuid = self.session.create_usecase('intra_vn', 'traffic')
#        self.session.validate_usecase(uuid) #Route validation, config pushed
#        uuid2 = self.session.create_flows(uuid)
#        self.session.validate_flows(uuid2)

    @pytest.mark.update
    def test_update_password(self):
        print('Updated password')

    @pytest.mark.delete
    def test_delete_users(self):
        print('Delete users from SP')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_service_provider(self):
        print('Deleting service provider account')
