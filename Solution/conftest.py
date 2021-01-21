import pytest
from .lib.session import PyTestSession

def pytest_addoption(parser):
    parser.addoption("--artifact", action="store", help="Artifact file location")
    parser.addoption("--user_input", action="store", help="User input file location")
    parser.addoption("--exec_id", action="store", help="Execution ID")
    parser.addoption("--product", action="store", help="Product identifier (eg: CEM, CN2)")

@pytest.fixture(scope="session", autouse=True)
def init_session(pytestconfig):
    artifact = pytestconfig.getoption('artifact')
    user_input = pytestconfig.getoption('user_input')
    exec_id = pytestconfig.getoption('exec_id')
    product = pytestconfig.getoption('product')
    print('artifact {} user_input {}'.format(artifact, user_input))
    PyTestSession(artifact, user_input, exec_id, product).initialize()
    yield
    PyTestSession().close()
