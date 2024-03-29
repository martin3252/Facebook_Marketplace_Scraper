import json

import requests
import streamlit as st

from GPT import call_GPT
from utils import postprocess_car_list

# Create a title for the web app.
st.title("Facebook Marketplace Vehichle Scraper")

# Add a list of supported cities.
supported_cities = ["Brisbane"]
supported_sortby = ["best_match", "price_ascend", "price_descend", "vehicle_mileage_ascend", "vehicle_mileage_descend", "vehicle_year_descend", "vehicle_year_ascend"]
supported_make = ["Toyota", "Honda", "Mazda", "all"]
supported_transmission = ["automatic", "manual"]
GPT_option = ["No", "Yes"]

# Take user input
city = st.selectbox("City", supported_cities, 0)
make_Type = st.selectbox("Make Type", supported_make, 0)
model_Type = st.text_input("Model")
min_year = st.text_input("Min Year", "2010")
max_year = st.text_input("Max Year", "2020")
min_price = st.text_input("Min Price", "10000")
max_price = st.text_input("Max Price", "15000")
min_mileage = st.text_input("Min Mileage", "50000")
max_mileage = st.text_input("Max Mileage", "150000")
transmission_Type = st.selectbox('transmission_Type', supported_transmission, 0)
radius = st.text_input('radius', '20')
sortBy = st.selectbox("Sort By", supported_sortby, 0)
GPT = st.selectbox("Enable GPT or not", GPT_option, 0)

# Create a button to submit the form.
submit = st.button("Submit")

# If the button is clicked.
if submit:
    # TODO - Remove any commas from the max_price before sending the request.
    if "," in max_price:
        max_price = max_price.replace(",", "")
    elif "," in min_price:
        min_price = min_price.replace(',', '')
    else:
        pass
    res = requests.get(
        f"http://127.0.0.1:8000/crawl_facebook_marketplace?city={city}&min_mileage={min_mileage}&max_mileage={max_mileage}&max_price={max_price}&min_price={min_price}&min_year={min_year}&max_year={max_year}&transmission_Type={transmission_Type}&make_Type={make_Type}&radius={radius}&sortBy={sortBy}&model_Type={model_Type}",
        timeout=1000,
    )

    # Convert the response from json into a Python list.
    results = res.json()

    # post-process results
    new_results = postprocess_car_list(results)

    if GPT == "Yes":
        # call_GPT
        GPT_results = call_GPT(new_results)

        # string to dict object
        GPT_results = json.loads(GPT_results)

    # Display the length of the results list.
    st.write(f"Number of results: {len(results)}")

    # Iterate over the results list to display each item.
    for item in results:
        st.header(item["title"])
        img_url = item["image"]
        st.image(img_url, width=200)
        st.write(item["price"])
        st.write(item['mileage'])
        st.write(item['transmission'])
        st.write(item["location"])
        st.write(f"https://www.facebook.com{item['link']}")
        st.write(item['msg'])
        st.write("----")
        if GPT == "Yes":
            st.write("GPT comment")

            for car, context in GPT_results.items():
                # print(gpt_car)
                st.write(car + ":" + context + '\n')
