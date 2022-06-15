import pytest

def pytest_addoption(parser):
    parser.addoption("--name", action="store", default="samuel")
    
def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.name
    if 'name' in metafunc.fixturenames and option_value is not None:
    	metafunc.parametrize("name", [option_value])
