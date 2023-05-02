# import smtplib

# gmail_user = 'bcalarm12345@gmail.com'
# gmail_password = 'suitcase12345'

# sent_from = gmail_user
# to = ['rowemg@gmail.com', 'zantaiyo@gmail.com']
# subject = 'Lorem ipsum dolor sit amet'
# body = 'consectetur adipiscing elit'

# email_text = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (sent_from, ", ".join(to), subject, body)

# try:
#     smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     smtp_server.ehlo()
#     smtp_server.login(gmail_user, gmail_password)
#     smtp_server.sendmail(sent_from, to, email_text)
#     smtp_server.close()
#     print("Email sent successfully!")
# except Exception as ex:
#     print("Something went wrong….", ex)

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


# import requests


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
    'Authorization': 'Basic MGRlZTI1MmQ2NzhhMGEwYzE0NDBiYzkzN2FmNjA4MTc6NGI3MjAwNjI4ODRkNzNkM2RhOTI5N2MyMWRlYjc1ZDY='
}

json_data = {
    'Messages': [
        {
            'From': {
                'Email': 'bcalarm12345@outlook.com',
                'Name': 'Mailjet Pilot',
            },
            'To': [
                {
                    'Email': 'rowemg@bc.edu',
                    'Name': 'passenger 1',
                },
            ],
            'Subject': 'Your email flight plan!',
            'TextPart': 'Dear passenger 1, welcome to Mailjet! May the delivery force be with you!',
            'HTMLPart': '<h3>Dear passenger 1, welcome to <a href="https://www.mailjet.com/">Mailjet</a>!</h3><br />May the delivery force be with you!',
        },
    ],
}

response = requests.post(
    'https://api.mailjet.com/v3.1/send',
    headers=headers,
    json=json_data
    # ,auth=(os.getenv('MJ_APIKEY_PUBLIC', ''),
    #       os.getenv('MJ_APIKEY_PRIVATE', '')),
)
print(response.text)
# at this point you could check the status etc
# this gets the page text

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n\t\t"Messages":[\n\t\t\t\t{\n\t\t\t\t\t\t"From": {\n\t\t\t\t\t\t\t\t"Email": "pilot@mailjet.com",\n\t\t\t\t\t\t\t\t"Name": "Mailjet Pilot"\n\t\t\t\t\t\t},\n\t\t\t\t\t\t"To": [\n\t\t\t\t\t\t\t\t{\n\t\t\t\t\t\t\t\t\t\t"Email": "passenger1@mailjet.com",\n\t\t\t\t\t\t\t\t\t\t"Name": "passenger 1"\n\t\t\t\t\t\t\t\t}\n\t\t\t\t\t\t],\n\t\t\t\t\t\t"Subject": "Your email flight plan!",\n\t\t\t\t\t\t"TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!",\n\t\t\t\t\t\t"HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\\"https://www.mailjet.com/\\">Mailjet</a>!</h3><br />May the delivery force be with you!"\n\t\t\t\t}\n\t\t]\n\t}'
# response = requests.post(
#    'https://api.mailjet.com/v3.1/send',
#    headers=headers,
#    data=data,
#    auth=(os.getenv('MJ_APIKEY_PUBLIC', ''), os.getenv('MJ_APIKEY_PRIVATE', '')),
# )
