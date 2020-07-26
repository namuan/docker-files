import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")


def notify_user(title, msg):
    try:
        response = requests.post(
            url="https://api.pushover.net/1/messages.json",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "message": msg,
                "title": title,
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER_KEY
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

notify_user("Docker files job", f"Completed")