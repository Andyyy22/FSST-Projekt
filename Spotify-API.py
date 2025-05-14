from dotenv import load_dotenv
import os
import base64
import random
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_song(token, song_name):
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_song_by_mood():
    mood_to_song = {
        "glücklich": ["Scream & Shout", "Einmal um die Welt"],
        "traurig": ["Umbrella", "Rather lie"],
        "sommer": ["Venedig", "2 Handys"],
        "chiller": ["Mittelmeer", "Juna", "Devil in a new Dress"],
        "gym": ["Berlin lebt", "Protection Charm"],
        "ballert" : ["Thx", "FE!N", "overseas"],
    }
    mood = input("Wie fühlst du dich? (glücklich, traurig, sommer, chiller, gym, ballert): ").strip().lower()
    if mood in mood_to_song:
        song_name = random.choice(mood_to_song[mood])
        song_data = search_song(token, song_name)
        songs = song_data.get("tracks", {}).get("items", [])
        if songs:
            song = songs[0]
            artist = song["artists"][0]["name"]
            print(f"\nDein perfekter Song:\nTitel: {song['name']}\nKünstler: {artist}\nDauer: {song['duration_ms'] // 1000} Sekunden")

        else:
            print("Kein Song gefunden.")
    else:
        print("Ungültige Stimmung.")

token = get_token()
get_song_by_mood()
