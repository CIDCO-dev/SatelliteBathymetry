import pytest

def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="username")
    parser.addoption("--password", action="store", default="password")
    
def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.username
    if 'username' in metafunc.fixturenames and option_value is not None:
    	metafunc.parametrize("username", [option_value])
    option_value = metafunc.config.option.password
    if 'password' in metafunc.fixturenames and option_value is not None:
    	metafunc.parametrize("password", [option_value])

