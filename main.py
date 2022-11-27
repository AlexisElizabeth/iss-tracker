import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 59.329323
MY_LONG = 18.068581
BUFFER = 5
TIME_ZONE = 2
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT - BUFFER <= iss_latitude <= MY_LAT + BUFFER and MY_LONG - BUFFER <= iss_longitude <= MY_LONG + BUFFER:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + TIME_ZONE
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + TIME_ZONE

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


if __name__ == "__main__":
    while True:
        time.sleep(60)
        if is_close() and is_night():
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"Subject:Look up!\n\nThe ISS is above you!")
