

import requests
import os
from flight_data import FlightData

KIWI_KEY = os.environ["kiwi_key"]
kiwi_url = "https://tequila-api.kiwi.com"
location_url = "/locations/query"

# https://api.tequila.kiwi.com/locations/query?term=Paris&locale=en-US&location_types=city&limit=10&active_only=true'
class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def find_iata(self, city: str):

        parameters = {
            "term": city,
            "locale": "en-US",
            "location_types": "city",
            "limit": 10,
            "active_only": "true",
        }

        response = requests.get(
            url=f"{kiwi_url}{location_url}",
            headers={"apikey": KIWI_KEY},
            params=parameters,
        )

        data = response.json()["locations"]

        return data[0]["code"]

    def search_flight(self, origin_iata, destination_iata, from_time, to_time):

        search_url = f"{kiwi_url}/v2/search"


        parameters = {
            "fly_from": origin_iata,
            "fly_to": destination_iata,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"

        }

        response = requests.get(
            url=search_url,
            headers={"apikey": KIWI_KEY},
            params=parameters,
        )
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights Found for {destination_iata}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
        )

        print(f'{flight_data.destination_city}: €{flight_data.price}')

        return flight_data

