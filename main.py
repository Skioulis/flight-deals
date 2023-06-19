# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from notification_manager import NotificationManager
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta

flights = DataManager()
notifications = NotificationManager()
ORIGIN_CITY_IATA = "LON"

sheet_data = flights.get_destinations()
flight_search = FlightSearch()
updated = False

for destination in sheet_data:
    if destination["iataCode"] == "":
        updated = True
        print("we are updating")

        destination["iataCode"] = flight_search.find_iata(destination["city"])

if updated:
    flights.destinations = sheet_data
    flights.update_iata()

today = datetime.now()
tomorrow = today + timedelta(days=1)
until = today + timedelta(days= 6*30)

for destination in sheet_data:

    flight = flight_search.search_flight(origin_iata=ORIGIN_CITY_IATA,
                                         destination_iata=destination["iataCode"],
                                         from_time=tomorrow, to_time=until)

    print(f"We found this a trip from {flight.origin_city} to {flight.destination_city} at {flight.out_date}"
          f" costing {flight.price}")
    notifications.send_mail(flight)
