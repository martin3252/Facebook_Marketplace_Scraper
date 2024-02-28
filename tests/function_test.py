import utils


def test_transmission():
    assert utils.check_transmission_type('auto transmission') == True
