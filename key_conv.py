import os
from base64 import b64encode


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode(
        'utf-8')).decode("ISO-8859-1")
    return f'Basic {token}'


username = "0dee252d678a0a0c1440bc937af60817"
password = "4b720062884d73d3da9297c21deb75d6"

out_val = basic_auth(username, password)
print(out_val)
