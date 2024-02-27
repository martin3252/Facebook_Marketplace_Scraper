import re


def check_transmission_type(transmission_type):
    if re.findall(r"transmission", transmission_type):
        return True

    return False
