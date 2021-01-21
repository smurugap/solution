import pytest
from Solution.lib.usecases import Usecases
from Solution.lib.session import PyTestSession
from Solution.lib.input import UserInput

class TestRestart(object):
    @pytest.mark.execute
    def test_restart_vrouter_agent(self):
        print('Running restart scenario in SaaS')
