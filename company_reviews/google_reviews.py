'''gets google reviews of company and returns a list fo the reviews'''

import requests
from bs4 import BeautifulSoup
import requests
import pandas as pd
from config import api_key # saved the api key in a config file and imported it

def google_reviews(comp_name):
    # place api url for getting the place id of the univeristy searched
    PLACE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    # place details api url for getting more details on the university
    # serached using the place id gotten from place api url
    DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json?"

    # combine the university name and the country name gotten from the country code
    query = comp_name

    # get the CCTLD which is will be needed to prioritize the country code given
    region = "ng"

    # GET request on places api
    place_response = requests.get(PLACE_URL + 'query=' \
        + query + '&key=' + api_key  + \
            '&region=' + region)

    data = place_response.json()

    # checks if places api returns zero results
    if not data['results']:
        return "no reviews"
    else:
        # obtain place id from place api response
        place_id = data['results'][0]['place_id']

        #GET request using the place id gotten from places api
        details_response = requests.get(DETAILS_URL + 'place_id=' + place_id + '&key=' + api_key)
        details_data = details_response.json()

        # obtain address details from place details response
        rev = details_data['result']['reviews']
        reviews = []
        for j in rev:
            reviews.append(j['text'])
        return reviews

comp_name = input("enter company name: ")
print(google_reviews(comp_name))