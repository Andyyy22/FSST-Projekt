import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
import threading
import base64
import random
from requests import post, get
import json

# Spotify-API Zugangsdaten direkt (ohne .env)
client_id = "79b3beae3f5841d9b51dbf9d5cec7689"
client_secret = "99b8eacc19ab4a61afeca0c9c7612600"

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
    if result.status_code != 200:
        print("Token Error:", result.text)
        return None
    return json.loads(result.content).get("access_token")

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_song(token, song_name):
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

# Emotion zu Song-Mapping
mood_to_song = {
    "happy":     ["Scream & Shout", "Einmal um die Welt"],
    "sad":       ["Umbrella", "Rather lie"],
    "neutral":   ["Mittelmeer", "Juna", "2 Handys"],
    "angry":     ["Berlin lebt", "Thx"],
    "surprise":  ["FE!N", "overseas"],
    "fear":      ["Don’t Fear The Reaper", "Scared to Be Lonely"],
    "disgust":   ["Bad Guy", "Creep"]
}

# Globale Variable für Emotion
current_emotion = "neutral"

def camera_loop():
    global current_emotion
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            faces = result if isinstance(result, list) else [result]
            for face in faces:
                region = face["region"]
                emotion = face["dominant_emotion"].lower()
                current_emotion = emotion

                x, y, w, h = region["x"], region["y"], region["w"], region["h"]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        except Exception as e:
            print("Analysefehler:", e)

        cv2.imshow("Live Emotionserkennung (q zum Beenden)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def song_auswahl():
    mood = current_emotion
    messagebox.showinfo("Aktuelle Emotion", f"Erkannt: {mood}")

    if mood in mood_to_song:
        song_name = random.choice(mood_to_song[mood])
        token = get_token()
        if token is None:
            messagebox.showerror("Fehler", "Spotify-Token konnte nicht abgerufen werden.")
            return

        data = search_song(token, song_name)
        tracks = data.get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            title = track["name"]
            artist = track["artists"][0]["name"]
            duration = track["duration_ms"] // 1000
            messagebox.showinfo(
                "Song Empfehlung",
                f"🎵 Titel: {title}\n👤 Künstler: {artist}\n⏱ Dauer: {duration}s"
            )
        else:
            messagebox.showwarning("Kein Treffer", "Spotify hat keinen Song gefunden.")
    else:
        messagebox.showerror("Unbekannte Emotion", f"Keine Songs definiert für: {mood}")

def start_gui():
    root = tk.Tk()
    root.title("Musik aus Emotion")
    root.geometry("300x200")

    tk.Label(root, text="Drücke den Button,\num einen Song zu bekommen", font=("Arial", 12)).pack(pady=20)
    tk.Button(root, text="Jetzt analysieren", command=song_auswahl,
              font=("Arial", 12), bg="lightblue").pack(pady=20)
    root.mainloop()

# Kamera starten und GUI öffnen
threading.Thread(target=camera_loop, daemon=True).start()
start_gui()
