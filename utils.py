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


def process_car_list_for_gpt(car_list):
    input_string = "```\n"
    # format gpt input
    for car in car_list:
        input_string = input_string + "car_index: " + str(car['car_index']) + '\n'
        input_string = input_string + "price: " + str(car["price"]) + '\n'
        input_string = input_string + "mileage: " + str(car["mileage"]) + '\n'
        input_string = input_string + "description: " + str(car["description"]) + '\n'
        input_string += "```\n"
    return input_string
