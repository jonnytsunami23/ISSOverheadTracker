import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = "jonathanestrada1001@gmail.com"
MY_PASSWORD = "Repr0bi23!"


MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(f"http://api.sunrise-sunset.org/json")
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


time_now = datetime.now().hour



#Your position is within +5 or -5 degrees of the ISS position.


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_latitude <= MY_LONG + 5:
        return True
def is_night():
    if time_now > sunset and time_now < sunrise:
        return True


def iss_is_visible():
    if is_night() and is_iss_overhead():
        return True
    else:
        return False

def send_email():
    if iss_is_visible():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg = "Subject: Look up^\n\n The ISS is above you in the sky."

        )
while True:
    time.sleep(60)
    send_email()
#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



