import os
import smtplib
from flight_data import FlightData

class NotificationManager:

    def send_mail(self, flight: FlightData):
        from_mail = os.environ["from_mail"]
        from_pass = os.environ["mail_pass"]
        to_mail = os.environ["to_mail"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=from_mail, password=from_pass)
            connection.sendmail(
                from_addr=from_mail,
                to_addrs=to_mail,
                msg=f"Subject:New deal for a requasted flight\n\nWe found this a trip from {flight.origin_city}"
                    f" to {flight.destination_city} at {flight.out_date} costing {flight.price}"
            )





