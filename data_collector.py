from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


def get_playlist_data(playlist_id, market):
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token = get_token(client_id, client_secret)
    json = get_playlist_reqest_url(access_token, playlist_id, market)
    return json


def get_token(client_id, client_secret):
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


def get_auth_header(access_token):
    return {"Authorization": "Bearer " + access_token}


def get_playlist_reqest_url(access_token, playlist_id, market):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}?{market}"
    query = get(url, headers=get_auth_header(access_token))
    return json.loads(query.content)
