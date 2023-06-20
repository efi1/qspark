"""Shared fixtures."""
import copy
import os # being used when evaluating settings
import yaml
from pathlib import Path  # being used in func: pytest_addoption
from pytest import fixture
from tests import settings
from src.utils.utils import dict_to_obj
from src.clients.client_requests import RequestesLocatesClient

settings_items = [i for i in settings.__dir__() if not i.startswith('_')]


def pytest_addoption(parser):
    """
    built-in pytest function to enable flags to be run via pytest
        e.g.   python -m pytest -<added flag by this func> <flag val>
    """
    for item in settings_items:
        try:
            value = eval(getattr(settings, item))
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            value = getattr(settings, item)
        parser.addoption(F"--{item}", action='store', default=value)


@fixture(scope="function")
def test_name(request):
    return request.node.name


@fixture(scope="session")
def tests_raw_data(request):
    """
    get all the tests' common data
    """
    raw_data = dict()
    for item in settings_items:
        raw_data[item] = request.config.getoption(F"--{item}")
    return raw_data


@fixture(scope="session")
def settings_data(tests_raw_data: dict) -> object:
    """
    Converting raw data of type dict to an object
    :param tests_raw_data: raw data input
    :return:
    """
    return dict_to_obj(tests_raw_data)


@fixture(scope="function")
def cfg_data(test_name) -> object:
    """
    :param test_name: the test name
    :return: test arguments only for non parametrized tests
    """
    test_name = test_name.split('[')[0]
    cfg_name = F'{test_name}.cfg'
    if not cfg_name.startswith('test_param'):
        cfg_template_dir = eval(settings.cfg_tests_folder)
        cfg_template_file = Path(cfg_template_dir).joinpath(cfg_name)
        if cfg_template_file.exists():
            with open(cfg_template_file, 'r') as cfg_data:
                cfg_data_dict = yaml.safe_load(cfg_data)
                return dict_to_obj(cfg_data_dict)


@fixture(scope="session")
def tests_client(settings_data: object) -> object:
    """
    :param settings_data: general data which required for the tests
    :return: initiate the client and return its instance
    """
    tests_client = RequestesLocatesClient(rsrc_path=settings_data.resources_folder)
    tests_client.load_data(settings_data.csv_file_name)
    yield tests_client


def load_test_params(test_name) -> object:
    """
    load all args which required only for the parametrized tests
    :param test_name: the test name
    :return: tests' arguments only for parametrized tests
    """
    test_name = test_name.split('[')[0]
    cfg_name = F'{test_name}.cfg'
    cfg_template_dir = eval(settings.cfg_tests_folder)
    cfg_template_file = Path(cfg_template_dir).joinpath(cfg_name)
    if cfg_template_file.exists():
        with open(cfg_template_file, 'r') as cfg_data:
            cfg_data_dict = yaml.safe_load(cfg_data)
            field_name = cfg_data_dict.get('field_name')
            approved_locates = cfg_data_dict.get('approved_locates')
            in_params = cfg_data_dict.get('in_params')
            expected_params = cfg_data_dict.get('expected_params')
            values = zip(in_params, expected_params, field_name, approved_locates)
            parameterized_data = cfg_data_dict.get('parameterized_data')
            parameterized_data[test_name]['values'] = values
            return parameterized_data


def pytest_generate_tests(metafunc):
    """
    generate the parametrized args which rewuired for the parametrized tests.
    :param metafunc: pytest built-in function
    """
    fct_name = metafunc.function.__name__
    if fct_name.startswith('test_param'):
        parameterized_data = load_test_params(fct_name)
        if parameterized_data.get(fct_name):
            params = parameterized_data[fct_name]
            metafunc.parametrize(params["params"], params["values"])

