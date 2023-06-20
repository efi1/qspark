import logging

logging.getLogger()


def test_param_devisible_by_100(req_inp, req_out, settings_data, tests_client, field_name, approved_locates, request):
    """
    Verify that the approved locates are calculated correctly and should be proportional to the requested sum.
    :param req_inp: customer request for locates of a specific symbol.
    :param req_out: server response (approved locates) for the customer request.
    :param settings_data: data which is taken from ~tests/settings.py - being parsed by conftest.py
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param field_name: the field to be gathered from - in our scope we used field=symbol
    :param approved_locates: the approved locate per each symbol.  e.g. {"ABC" : 480, "QQQ" : 445, "TTT" : 210.12}
    :param request: internal pytest object which is needed to get the iteration number.
    """
    # calc is to be run only at first iteration, since input doesn't change, there is no need to recalculate.
    if request.node.name.split('[')[1].split('-')[0].endswith('inp0'):
        tests_client.calc_approved_locates_by_client(field_name, approved_locates)
    res = tests_client.request_locates(req_inp)
    assert res == req_out, F"wrong approved locates; total approved: {approved_locates} locates, expected:" \
                            F" {req_out}, found: {res}"


def test_param_not_divisible_by_100(req_inp, req_out, tests_client, field_name, approved_locates, request):
    """
    Verify that the approved locates are calculated correctly when total approved chunks per symbol isn't divisible by 100.
    :param req_inp: customer request for locates of a specific symbol.
    :param req_out: server response (approved locates) for the customer request.
    :param tests_client: the software client which is being used for query the input data (csv with locates)
    :param field_name: the field to be gathered from - in our scope we used field=symbol
    :param approved_locates: the approved locate per each symbol.  e.g. {"ABC" : 480, "QQQ" : 445, "TTT" : 210.12}
    :param request: internal pytest object which is needed to get the iteration number.
    """
    if request.node.name.split('[')[1].split('-')[0].endswith('inp0'):  # to be run only at first iteration only
        tests_client.calc_approved_locates_by_client(field_name, approved_locates)
    res = tests_client.request_locates(req_inp)
    assert res == req_out, F"wrong approved locates; total approved: {approved_locates} locates, expected:" \
                            F" {req_out}, found: {res}"


def test_param_approved_less_than_100(req_inp, req_out, tests_client, field_name, approved_locates, request):
    """
    Verify that the approved locates are calculated correctly when total approved is smaller a 100 chunk.
    """
    if request.node.name.split('[')[1].split('-')[0].endswith('inp0'):  # to be run only at first iteration only
        tests_client.calc_approved_locates_by_client(field_name, approved_locates)
    res = tests_client.request_locates(req_inp)
    assert res == req_out, F"wrong approved locates; total approved: {approved_locates} locates, expected:" \
                            F" {req_out}, found: {res}"


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

