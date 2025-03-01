import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 21.352381
MY_LONG = 74.880127

my_email = "testmail020906@gmail.com"
my_pass = "owepnvzjczutunoi"

def is_overhead():

    global MY_LONG, MY_LAT

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (iss_latitude < MY_LAT+5 and iss_latitude > MY_LAT-5) and (iss_longitude < MY_LONG+5 and iss_longitude > MY_LONG-5):
        return True
    else:
        return False

#Your position is within +5 or -5 degrees of the ISS position.

def is_visible():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5

    time_now = datetime.now()
    current_hour = time_now.hour

    if current_hour > sunset or current_hour < sunrise:
        return True
    else:
        return False

while True:

    if is_visible() and is_overhead():

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(my_email, my_pass)
            connection.sendmail(from_addr = my_email,
                                to_addrs = "yc.nitin.01@gmail.com",
                                msg = "Subject:Look Above!\n\nThe Internation Space Station is now visible near you!!\nGo outside and look above!")

    time.sleep(60)
