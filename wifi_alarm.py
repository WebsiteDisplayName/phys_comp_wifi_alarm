# outlook login
# gmail_user = 'bcalarm12345@outlook.com'
# gmail_password = 'suitcase12345'


# import wifi
# mac_address = [f"{i:02x}" for i in wifi.radio.mac_address]
# print(':'.join(mac_address))

import board
import adafruit_requests
import socketpool
import wifi
import ssl
import time
import os
import rtc
import circuitpython_schedule as schedule


clock = rtc.RTC()

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
# wifi.radio.connect(os.getenv("x"), os.getenv("y"))
print("Connected to Wifi")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# https://timeapi.io/swagger/index.html
url = "https://timeapi.io/api/Time/current/zone?timeZone="
timezone = "America/New_York"
url += timezone
response = requests.get(url)
json = response.json()


def ret_time(json_obj):
    day = json_obj['dayOfWeek']
    date = json_obj['date']
    time = json_obj['time']
    timezone = json_obj['timeZone']

    comb_time = f"{timezone}: {day}, {date} {time}"
    return comb_time


print(json)
print(json['time'])
print(ret_time(json))


# Authorization token: we need to base 64 encode it
# and then decode it to acsii as python 3 stores it as a byte string

# base64
# from base64 import b64encode
# def basic_auth(username, password):
#     token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
#     return f'Basic {token}'

# username = os.getenv("MJ_APIKEY_PUBLIC")
# password = os.getenv("MJ_APIKEY_PRIVATE")

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv("COMB_KEY")
}

json_data = {
    'Messages': [
        {
            'From': {
                'Email': 'bcalarm12345@outlook.com',
                'Name': 'Assistive Tech Alarm',
            },
            'To': [
                {
                    'Email': 'rowemg@bc.edu',
                    'Name': 'passenger 1',
                },
            ],
            'Subject': 'The Alarm Button Was Pressed!',
            'TextPart': 'Dear passenger 1, welcome to Mailjet! May the delivery force be with you!',
            'HTMLPart': '<h3>Dear passenger 1, welcome to <a href="https://www.mailjet.com/">Mailjet</a>!</h3><br />May the delivery force be with you!',
        },
    ],
}

response = requests.post(
    'https://api.mailjet.com/v3.1/send',
    headers=headers,
    json=json_data
)
print(response.text)
