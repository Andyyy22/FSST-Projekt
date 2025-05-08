import requests
import random

mood_to_song = {
    "glücklich": ["bohemian", "Walking on Sunshine"],
    "traurig": ["Someone Like You","Let Her Go"],
    "gym": ["Eye of the Tiger", "Lose Yourself"],
    "random": ["Believer", "Blinding Lights"]
}

mood = input("Wie fühlst du dich? (glücklich, traurig, gym, random): ").strip().lower()

if mood in mood_to_song:
    song_name = random.choice(mood_to_song[mood])

    url = f"https://osdb-api.confidence.sh/rest/aC-5hURuqrEEcnDVPKC8R/search/song?query={song_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        songs = data.get("data", [])
        if songs:
            song = songs[0]
            print(f"\nDein perfekter Song:\nTitel: {song['name']}\nDauer: {song['duration']}")
        else:
            print("Kein Song gefunden.")
    else:
        print("Fehler bei der Anfrage.")
else:
    print("Ungültige Stimmung.")
