import os
import requests
from pprint import pprint

SHEETY_ENDPOINT = os.environ['sheety_endpoint']
SHEETY_USER = os.environ["sheety_user"]
SHEETY_PASS = os.environ["sheety_pass"]
SHEETY_EMAIL = os.environ['sheety_email']
SHEETY_PROJECT = "flightdeals"
SHEETY_SHEET = "prices"

endpoint = f"https://api.sheety.co/{SHEETY_USER.lower()}/{SHEETY_PROJECT}/{SHEETY_SHEET}"

sheety_auth = {
    SHEETY_USER,
    SHEETY_PASS,
}



class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destinations = {}

    def get_destinations(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()
        self.destinations = response.json()['prices']

        return self.destinations

    def update_iata(self):
        for city in self.destinations:
            data_to_update = {
                "price" : {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=data_to_update
            )
            print(response.text)
