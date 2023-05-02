# outlook login
# gmail_user = 'bcalarm12345@outlook.com'
# gmail_password = 'suitcase12345'

# mailjet
# gmail_user = 'bcalarm12345@outlook.com'
# gmail_password = 'suitcase12345+'
#

# import wifi
# mac_address = [f"{i:02x}" for i in wifi.radio.mac_address]
# print(':'.join(mac_address))

import digitalio
from adafruit_debouncer import Button
import board
import adafruit_requests
import socketpool
import wifi
import ssl
import time
import os
import rtc
import circuitpython_schedule as schedule
import board
import neopixel
from adafruit_led_animation.animation.rainbow import Rainbow

strip = neopixel.NeoPixel(board.GP14, 30)
rainbow_strip = Rainbow(strip, speed=0.05, period=2)

button_input = digitalio.DigitalInOut(board.GP15)  # Wired to GP15
# Note: Pull.UP for external buttons
button_input.switch_to_input(digitalio.Pull.UP)
button = Button(button_input)  # NOTE: False for external buttons

clock = rtc.RTC()

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
# wifi.radio.connect(os.getenv("x"), os.getenv("y"))
print("Connected to Wifi")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# https://timeapi.io/swagger/index.html
time_url = "https://timeapi.io/api/Time/current/zone?timeZone="
timezone = "America/New_York"
time_url += timezone


def ret_time(time_url):
    time_response = requests.get(time_url)
    time_json = time_response.json()
    day = time_json['dayOfWeek']
    date = time_json['date']
    time = time_json['time']
    timezone = time_json['timeZone']

    comb_time = f"{timezone}: {day}, {date} {time}"
    return comb_time

# https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
# Authorization token: we need to base 64 encode it
# and then decode it to acsii as python 3 stores it as a byte string

# base64
# from base64 import b64encode
# def basic_auth(username, password):
#     token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
#     return f'Basic {token}'

# username = os.getenv("MJ_APIKEY_PUBLIC")
# password = os.getenv("MJ_APIKEY_PRIVATE")

# mailjet API provider: https://dev.mailjet.com/email/guides/send-api-V3/
# https://curlconverter.com/


def post_request(text_file_name):

    with open(text_file_name) as f:
        email_list = [email.strip() for email in f]

    to_dict_list = []
    for email in email_list:
        tempDict = dict()
        tempDict['Email'] = email
        tempDict['Name'] = ''
        to_dict_list.append(tempDict)

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
                'To': to_dict_list,
                'Subject': 'The Alarm Button Was Pressed!',
                'TextPart': f'Sent: {ret_time(time_url)}',
            },
        ],
    }

    response = requests.post(
        'https://api.mailjet.com/v3.1/send',
        headers=headers,
        json=json_data
    )
    print(response.status_code)


rainbow_strip.fill((0, 0, 0))

print("Loop")
while True:
    button.update()  # Gets current state of button
    if button.pressed:  # True if pressed
        print("PRESSED")
        for idx in range(20):
            rainbow_strip.animate()
            time.sleep(0.2)
        post_request("target_emails.txt")
        rainbow_strip.fill((0, 0, 0))
