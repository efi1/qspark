import pytest
import logging

logging.getLogger()

in_params = [{"client_name": "Client1", 'symbol': "TTT", "number_of_locates_requested": 100},
             {"client_name": "Client2", 'symbol': "TTT", "number_of_locates_requested": 200},
             {"client_name": "Client3", 'symbol': "TTT", "number_of_locates_requested": 100},
             {"client_name": "Client4", 'symbol': "TTT", "number_of_locates_requested": 100}]

expected_params = [{'client_name': 'Client1', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100},
                   {'client_name': 'Client2', 'symbol': 'TTT', 'req_locates': 200, 'approved_locates': 200},
                   {'client_name': 'Client3', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100},
                   {'client_name': 'Client4', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100}]


@pytest.mark.parametrize("inp,expected", zip(in_params, expected_params))
def test_devisible_by_100(inp, expected, settings_data, tests_client, cfg_data, request):
    """
    Verify that the approved locates are calculated correctly and should be proportional to the requested sum.
    :param inp: customer request for locates of a specific symbol.
    :param expected: server response (approved locates) for the customer request.
    :param settings_data: data which is taken from ~tests/settings.py - being parsed by conftest.py
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param cfg_data: the test's arguments.
    :param request: internal pytest object which is needed to get the iteration number.
    """
    # calc is to be run only at first iteration, since input doesn't change, there is no need to recalculate.
    if request.node.name.split('[')[1].split('-')[0] == 'inp0':
        tests_client.calc_approved_locates_by_client(cfg_data.field_name, cfg_data.approved_locates)
    res = tests_client.request_locates(inp)
    assert res == expected, F"wrong approved locates; total approved: {cfg_data.approved_locates} locates, expected:" \
                            F" {expected}, found: {res}"


expected_params = [{'client_name': 'Client1', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100},
                   {'client_name': 'Client2', 'symbol': 'TTT', 'req_locates': 200, 'approved_locates': 199.326},
                   {'client_name': 'Client3', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100},
                   {'client_name': 'Client4', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 100}]


@pytest.mark.parametrize("inp,expected", zip(in_params, expected_params))
def test_not_divisible_by_100(inp, expected, tests_client, cfg_data, request):
    """
    Verify that the approved locates are calculated correctly when total approved chunks per symbol isn't divisible by 100.
    :param inp: customer request for locates of a specific symbol.
    :param expected: server response (approved locates) for the customer request.
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param cfg_data: the test's arguments.
    :param request: internal pytest object which is needed to get the iteration number.
    """
    if request.node.name.split('[')[1].split('-')[0] == 'inp0': # to be run only at first iteration only
        tests_client.calc_approved_locates_by_client(cfg_data.field_name, cfg_data.approved_locates)
    res = tests_client.request_locates(inp)
    assert res == expected, F"wrong approved locates; total approved: {cfg_data.approved_locates} locates, expected:" \
                            F" {expected}, found: {res}"


expected_params = [{'client_name': 'Client1', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 49.326},
                   {'client_name': 'Client2', 'symbol': 'TTT', 'req_locates': 200, 'approved_locates': 0},
                   {'client_name': 'Client3', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 0},
                   {'client_name': 'Client4', 'symbol': 'TTT', 'req_locates': 100, 'approved_locates': 0}]


@pytest.mark.parametrize("inp,expected", zip(in_params, expected_params))
def test_approved_less_than_100(inp, expected, tests_client, cfg_data, request):
    """
    Verify that the approved locates are calculated correctly when total approved is smaller a 100 chunk.
    """
    if request.node.name.split('[')[1].split('-')[0] == 'inp0': # to be run only at first iteration only
        tests_client.calc_approved_locates_by_client(cfg_data.field_name, cfg_data.approved_locates)
    res = tests_client.request_locates(inp)
    assert res == expected, F"wrong approved locates; total approved: {cfg_data.approved_locates} locates, expected:" \
                            F" {expected}, found: {res}"


def test_neg_missing_client_request(tests_client, cfg_data):
    """
    Verify that a correct error received when a non-valid request is made (a customer who hasn't requested locates,
    but checks later if they are approved).
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param cfg_data: the test's arguments.
    """
    tests_client.calc_approved_locates_by_client(cfg_data.field_name, cfg_data.approved_locates)
    res = str(tests_client.request_locates(cfg_data.request))
    assert res == cfg_data.approved, F"client request for {cfg_data.request['client_name']} shouldn't exist"


def test_neg_approved_bigger_than_requested(tests_client, cfg_data):
    """
    Verify that a correct error received when a non-valid request approval was made (the server approved more than
     was requested).
    but checks later if they are approved).
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param cfg_data: the test's arguments.
    """
    tests_client.calc_approved_locates_by_client(cfg_data.field_name, cfg_data.approved_locates)
    res = str(tests_client.request_locates(cfg_data.request))
    assert res == cfg_data.approved, F"client request for {cfg_data.request['client_name']} shouldn't exist"