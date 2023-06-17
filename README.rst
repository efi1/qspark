=====================
Q-Spark Assignment
=====================

The assignment includes several tests which verify server request functionality .

Test1:     Verify that the approved locates are calculated correctly and should be proportional to the requested sum.
Test2:     Verify that the approved locates are calculated correctly when total approved chunks per symbol isn't divisible
    by 100.
Test3:     Verify that a correct error received when a non-valid request is made (a customer who hasn't requested locates,
    but checks later if they are approved).
Test4:     Verify that a correct error received when a non-valid request approval was made (the server approved more than
     was requested).

Usage:

- Please use python virtual env.
- Since the tested were verified in Python 3.11 environment.
- Run "python setup.py install" (run it first) - setp.py is placed under the project folder.

- All testing variables resides in settings.py under the tests folder as well as under cfg_tests folder.
- Setting variables can be updated directly through the settings.py or can alternatively be used by the command
 line as flags ( e.g. python -m pytest --<flag_name> <execution value> ).
 If not using a flag for a certain variable it will be taken from the setting.py
- cfg_tests folder contains four files (cfg file for each test) and contains the test's args and the required data
 for running it.

- You might use the configured pytest marker "slow" to avoid running any of the tests
(e.g. python -m pytest -m "not slow").
  Using "slow" flag also required to mark the test with @pytest.Mark.slow)
- Running log is configured at the pytest.ini and is printed to that console and written into logfile.log as well.
(log level can be changed within the pytest.ini file).

