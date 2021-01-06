import pytest

class TestvEPC(object):
    @classmethod
    def setup_class(cls):
#        logger.info("Inside setup_class")
        print('Inside setup_class')

    @pytest.mark.onboard
    def test_onboard_service_provider(self):
        print('onboarded SP')

    @pytest.mark.update
    def test_add_new_user(self):
        print('Updated password')

    @pytest.mark.delete
    def test_restart_vrouter_agent(self):
        print('Restart vRouter agent service')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_service_provider(self):
        print('Deleting service provider account')
