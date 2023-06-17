"""Shared fixtures."""
import os # being used when evaluating settings
import yaml
from pathlib import Path  # being used in func: pytest_addoption
from pytest import fixture
from tests import settings
from src.utils.utils import dict_to_obj
from src.clients.client_requests import RequestesLocatesClient

settings_items = [i for i in settings.__dir__() if not i.startswith('_')]


def pytest_addoption(parser):
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
    test_name = test_name.split('[')[0]
    cfg_name = F'{test_name}.cfg'
    cfg_template_dir = eval(settings.cfg_tests_folder)
    cfg_template_file = Path(cfg_template_dir).joinpath(cfg_name)
    if cfg_template_file.exists():
        with open(cfg_template_file, 'r') as cfg_data:
            cfg_data_dict = yaml.safe_load(cfg_data)
            return dict_to_obj(cfg_data_dict)


@fixture(scope="session")
def tests_client(settings_data: object) -> object:
    tests_client = RequestesLocatesClient(rsrc_path=settings_data.resources_folder)
    tests_client.load_data(settings_data.csv_file_name)
    yield tests_client

