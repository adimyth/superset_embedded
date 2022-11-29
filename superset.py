import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


URL_AUTH = os.getenv("URL_AUTH")
URL_GUEST_TOKEN = os.getenv("URL_GUEST_TOKEN")
USERNAME = os.getenv("USERNAME")
FIRST_NAMER = os.getenv("FIRST_NAMER")
LAST_NAME = os.getenv("LAST_NAME")


def authenticate(
    username="admin",
    password="admin",
):
    response = requests.post(
        "http://localhost:8088/api/v1/security/login",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:8000",
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
    return response.json()["access_token"]


def get_guest_token_for_dashboard(
    dashboard_id,
    access_token,
    username=USERNAME,
    first_name=FIRST_NAMER,
    last_name=LAST_NAME,
):
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
    return response.json()["token"]
