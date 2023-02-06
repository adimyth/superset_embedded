import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


URL_AUTH = os.getenv("URL_AUTH")
URL_GUEST_TOKEN = os.getenv("URL_GUEST_TOKEN")
USERNAME = os.getenv("USERNAME")
FIRST_NAME = os.getenv("FIRST_NAME")
LAST_NAME = os.getenv("LAST_NAME")
print('URL_AUTH:', URL_AUTH)
print('URL_GUEST_TOKEN:', URL_GUEST_TOKEN)
print('USERNAME:', USERNAME)
print('FIRST_NAME:', FIRST_NAME)
print('LAST_NAME:', LAST_NAME)

def authenticate(
    username="admin",
    password="admin",
):
    print('Start authenticate')
    response = requests.post(
        # "http://localhost:8088/api/v1/security/login",
        # headers={
        #     "Content-Type": "application/json",
        #     "Accept": "application/json",
        #     "Access-Control-Allow-Origin": "http://localhost:8000",
        # },
        URL_AUTH,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data=json.dumps(
            {
                "username": username,
                "password": password,
                "provider": "db",
                "refresh": True
            }
        ),
    )
    print('authenticate response:', response)
    # print('response.json:', response.json())
    print('access_token: ', response.json()["access_token"])
    print('refresh_token: ', response.json()["refresh_token"])
    return response.json()["access_token"]


def get_guest_token_for_dashboard(
    dashboard_id,
    access_token,
    username=USERNAME,
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
):
    print('dashboard_id: ', dashboard_id)
    # print('auth access_token: ', access_token)
    response = requests.post(
        URL_GUEST_TOKEN,
        data=json.dumps(
            {
                "user": {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                },
                "resources": [
                    {
                        "type": "dashboard",
                        "id": dashboard_id,
                    }
                ],
                "rls": [],
            }
        ),
        headers={
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    print('get_guest_token_for_dashboard response:', response)
    return response.json()["token"]
