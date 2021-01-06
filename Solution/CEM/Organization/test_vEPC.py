import pytest

class TestvEPC(object):
    @pytest.mark.update
    def test_create_endpoints(self):
        print('Create a subscriber and validate subscriber traffic been routed')

    @pytest.mark.run('last')
    @pytest.mark.teardown
    def test_delete_endpoints(self):
        print('Deleting bgpaas service')
