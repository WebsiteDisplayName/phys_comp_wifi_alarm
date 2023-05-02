import os
from base64 import b64encode


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode(
        'utf-8')).decode("ISO-8859-1")
    return f'Basic {token}'


public_key = "public key numbers"
private_key = "private key numbers"

out_val = basic_auth(public_key, private_key)
print(out_val)
