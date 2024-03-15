# Description: This file contains the code for Passivebot's Facebook Marketplace Scraper API.
# Date: 2024-02-26
# Author: Martin Huang
# Version: 1.0.0.
# Usage: python app.py

# The time library is used to add a delay to the script.
import time

# The uvicorn library is used to run the API.
import uvicorn

# The BeautifulSoup library is used to parse the HTML.
from bs4 import BeautifulSoup

# The FastAPI library is used to create the API.
from fastapi import FastAPI, HTTPException

# Playwright is used to crawl the Facebook Marketplace.
from playwright.sync_api import sync_playwright
from fastapi.middleware.cors import CORSMiddleware

from utils import check_transmission_type

# Create an instance of the FastAPI class.
app = FastAPI()
# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Create a route to the root endpoint.
@app.get("/")
# Define a function to be executed when the endpoint is called.
def root():
    # pylint: disable=line-too-long
    # Return a message.
    return {
        "message": "Welcome to Passivebot's Facebook Marketplace API. \
         Documentation is currently being worked on along with the API. \
         Some planned features currently in the pipeline are a ReactJS frontend, MongoDB database, and Google Authentication."
    }

    # TODO - Add documentation to the API.
    # TODO - Add a React frontend to the API.
    # TODO - Add a MongoDB database to the API.
    # TODO - Add Google Authentication to the React frontend.


# Create a route to the return_data endpoint.
@app.get("/crawl_facebook_marketplace")
# Define a function to be executed when the endpoint is called.
# Add a description to the function.
def crawl_facebook_marketplace(
    city: str,
    max_price: int,
    min_price: int,
    min_year: int,
    max_year: int,
    transmission_Type: str,
    make_Type: str,
    radius: int,
    sortBy: str,
    min_mileage: int,
    max_mileage: int,
    model_Type: str,
):
    # pylint: disable=line-too-long
    # Define dictionary of cities from the facebook marketplace directory for United States.
    # https://m.facebook.com/marketplace/directory/US/?_se_imp=0oey5sMRMSl7wluQZ
    # TODO - Add more cities to the dictionary.
    if make_Type == "all":
        make_Type = ""
    cities = {"Brisbane": "brisbane"}
    # If the city is in the cities dictionary...
    if city in cities:
        # Get the city location id from the cities dictionary.
        city = cities[city]
    # If the city is not in the cities dictionary...
    else:
        # Exit the script if the city is not in the cities dictionary.
        # Capitalize only the first letter of the city.
        city = city.capitalize()
        # Raise an HTTPException.
        raise HTTPException(
            404,
            f"{city} is not a city we are currently supporting on the Facebook Marketplace. Please reach out to us to add this city in our directory.",
        )
        # TODO - Try and find a way to get city location ids from Facebook if the city is not in the cities dictionary.

    # Define the URL to scrape.
    marketplace_url = f"https://www.facebook.com/marketplace/{city}/vehicles?&minMileage={min_mileage}&maxMileage={max_mileage}&maxPrice={max_price}&minPrice={min_price}&minYear={min_year}&maxYear={max_year}&transmissionType={transmission_Type}&make={make_Type}&radius={radius}&sortBy={sortBy}&model={model_Type}"
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"
    # Get listings of particular item in a particular city for a particular price.
    # Initialize the session using Playwright.
    with sync_playwright() as p:
        # Open a new browser page.
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the URL.
        page.goto(initial_url)
        # Wait for the page to load.
        time.sleep(2)
        try:
            email_input = page.wait_for_selector('input[name="email"]').fill("YOUR_EMAIL_HERE")
            password_input = page.wait_for_selector('input[name="pass"]').fill("YOUR_PASSWORD_HERE")
            time.sleep(2)
            login_button = page.wait_for_selector('button[name="login"]').click()
            time.sleep(2)
            page.goto(marketplace_url)
            time.sleep(2)
            # close login information
            button = page.query_selector('div[aria-label="Close"]')
            button.click()

        except:
            page.goto(marketplace_url)
        # Wait for the page to load.
        time.sleep(2)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        parsed = []
        listings = soup.find_all(
            "div",
            class_="x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24",
        )
        for listing in listings[:2]:
            new_page = browser.new_page()
            try:
                # Get the item image.
                image = listing.find("img", class_="xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3")["src"]
                # Get the item title from span.
                title = listing.find("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6").get_text()
                # Get the item price.
                price = listing.find(
                    "span",
                    class_="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u",
                ).get_text()
                # Get the item URL.
                post_url = listing.find(
                    "a",
                    class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv",
                )["href"]
                # Get the item location and mileage.
                datas = listing.find_all("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft")
                for index, d in enumerate(datas):
                    # Get location
                    if index == 0:
                        location = d.get_text()
                    # Get mileage
                    else:
                        mileage = d.get_text()

                # Get seller message
                new_page.goto(f"https://www.facebook.com{post_url}")
                # print(f"https://www.facebook.com{post_url}")

                html = new_page.content()
                soup = BeautifulSoup(html, "html.parser")
                ### close the login notice

                button = new_page.query_selector('div[aria-label="Close"]')
                button.click()
                time.sleep(3)
                see_more_buttons = new_page.query_selector_all('span:has-text("See more")')
                see_more_buttons[-1].click()
                time.sleep(2)

                html = new_page.content()
                soup = BeautifulSoup(html, "html.parser")

                listing_msg = soup.find_all(
                    "span",
                    class_="x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u",
                )

                transmission = ""
                msg = ""
                for index, l in enumerate(listing_msg):

                    l = l.get_text()
                    # print(l)
                    if check_transmission_type(l):
                        transmission = l
                    elif index == 5:
                        msg = l.replace(" See less", "")
                time.sleep(2)
                new_page.close()
                # Append the parsed data to the list.
                parsed.append(
                    {
                        "image": image,
                        "title": title,
                        "price": price,
                        "post_url": post_url,
                        "location": location,
                        "msg": msg,
                        "mileage": mileage,
                        "transmission": transmission,
                    }
                )
            except:
                new_page.close()
        # Close the browser.
        browser.close()
        # Return the parsed data as a JSON.
        result = []
        for item in parsed:
            result.append(
                {
                    "name": item["title"],
                    "price": item["price"],
                    "location": item["location"],
                    "title": item["title"],
                    "image": item["image"],
                    "link": item["post_url"],
                    "msg": item["msg"],
                    "mileage": item["mileage"],
                    "transmission": item["transmission"],
                }
            )
        return result


# Create a route to the return_html endpoint.
@app.get("/return_ip_information")
# Define a function to be executed when the endpoint is called.
def return_ip_information():
    # pylint: disable=line-too-long
    # pylint: disable=
    # Initialize the session using Playwright.
    with sync_playwright() as p:
        # Open a new browser page.
        browser = p.chromium.launch()
        page = browser.new_page()
        # Navigate to the URL.
        page.goto("https://www.ipburger.com/")
        # Wait for the page to load.
        time.sleep(5)
        # Get the HTML content of the page.
        html = page.content()
        # Beautify the HTML content.
        soup = BeautifulSoup(html, "html.parser")
        # Find the IP address.
        ip_address = soup.find("span", id="ipaddress1").text
        # Find the country.
        country = soup.find("strong", id="country_fullname").text
        # Find the location.
        location = soup.find("strong", id="location").text
        # Find the ISP.
        isp = soup.find("strong", id="isp").text
        # Find the Hostname.
        hostname = soup.find("strong", id="hostname").text
        # Find the Type.
        ip_type = soup.find("strong", id="ip_type").text
        # Find the version.
        version = soup.find("strong", id="version").text
        # Close the browser.
        browser.close()
        # Return the IP information as JSON.
        return {
            "ip_address": ip_address,
            "country": country,
            "location": location,
            "isp": isp,
            "hostname": hostname,
            "type": ip_type,
            "version": version,
        }


if __name__ == "__main__":

    # Run the app.
    uvicorn.run(
        # Specify the app as the FastAPI app.
        "app:app",
        host="127.0.0.1",
        port=8000,
    )
