#!/usr/bin/env python3

import uuid
import json
import requests

REST_PATH = '/api/v1.0/devices/'

def get_device_id():
    """
    MAC address in integer format.
    """
    return uuid.getnode()

def send(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        url += REST_PATH + str(get_device_id())
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r)
    except Exception as e:
        print('Cannot send data: ', repr(e))
