import re
import pytest
from Tests.Solution.lib import session

def pytest_addoption(parser):
    parser.addoption("--artifact", action="store", help="Artifact file location")
    parser.addoption("--user_input", action="store", help="User input file location")
    parser.addoption("--exec_id", action="store", help="Execution ID")

@pytest.fixture(scope="session", autouse=True)
def init_session(pytestconfig):
    artifact = pytestconfig.getoption('artifact')
    user_input = pytestconfig.getoption('user_input')
    exec_id = pytestconfig.getoption('exec_id')
    print('artifact {} user_input {}'.format(artifact, user_input))
    session.Session(artifact, user_input, exec_id).initialize()
    yield
    session.Session().write_back()
