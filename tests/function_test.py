import utils


def test_regular_experssion():
    result = utils.check_transmission_type("automatic transmission")
    assert result == True
