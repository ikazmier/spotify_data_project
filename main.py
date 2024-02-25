from dotenv import load_dotenv
import os
import base64
from requests import post
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_base64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=form)
    json_result = json.loads(result.content)
    access_token = json_result["access_token"]

    if result.status_code != 200:
        print("Failed to retrieve token")
        print(f"Status Code: {result.status_code}")
        print(f"Response: {result.text}")
        return None

    return access_token


json_result = get_token()
print(json_result)
