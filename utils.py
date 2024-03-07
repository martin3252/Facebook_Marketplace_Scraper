import re


def check_transmission_type(transmission_type):
    if re.findall(r"transmission", transmission_type):
        return True

    return False


def single_quotes_to_two_quotes(origin_str):
    p = re.compile('(?<!\\\\)\'')
    new_str = p.sub('\"', origin_str)
    return new_str


def postprocess_car_list(car_list):
    car_list_for_gpt = []
    for index, r in enumerate(car_list):
        new_r = {}
        new_r["car_index"] = index + 1
        price = re.search(r'[\d,]+', r["price"])
        new_r["price"] = price.group(0)
        new_r["mileage"] = r["mileage"]
        new_r["description"] = r["msg"]
        car_list_for_gpt.append(new_r)
    return car_list_for_gpt
