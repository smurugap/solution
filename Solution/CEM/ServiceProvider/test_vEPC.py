import pytest

class TestvEPC(object):
    @classmethod
    def setup_class(cls):
#        logger.info("Inside setup_class")
        print('Inside setup_class')

    @pytest.mark.onboard
    def test_onboard_organizations(self):
        print('onboarded organizations')

    @pytest.mark.onboard
    def test_create_bgpaas(self):
        print('create bgpaas')
#        IntraVN()
#        uuid = self.session.create_usecase('intra_vn', 'traffic')
#        self.session.validate_usecase(uuid) #Route validation, config pushed
#        uuid2 = self.session.create_flows(uuid)
#        self.session.validate_flows(uuid2)

    @pytest.mark.update
    def test_change_asn(self):
        print('Updated ASN attribute of bgpaas object')

    @pytest.mark.delete
    def test_restart_vm(self):
        print('Restart vMX server')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_teardown_bgpaas(self):
        print('Deleting bgpaas service')
