Hallo unsere Namen sind Andreas und Marco.
# Emotionserkennung mit Songvorschlägen via Spotify 🎧🧠

Dieses Python-Projekt erkennt deine aktuelle Emotion über die Webcam und schlägt dir auf Basis dessen einen passenden Song vor – mithilfe der Spotify-API.
Die Anwendung kombiniert künstliche Intelligenz (DeepFace), Computer Vision (OpenCV) und eine intuitive grafische Oberfläche (Tkinter).

---

Verwendete Bibliotheken

Folgende Python-Bibliotheken werden verwendet:

| Bibliothek        | Zweck                                      |
|-------------------|--------------------------------------------|
| `opencv-python`   | Webcam-Zugriff & Bildanzeige               |
| `deepface`        | Emotionserkennung auf Gesichtern           |
| `tkinter`         | Grafische Benutzeroberfläche (GUI)         |
| `requests`        | HTTP-Anfragen an die Spotify-API           |
| `base64`          | Kodierung der API-Zugangsdaten             |
| `random`          | Zufällige Songauswahl aus Liste            |
| `json`            | Verarbeitung von API-Antworten             |
| `threading`       | Gleichzeitige Ausführung von GUI & Kamera  |

---
So funktioniert die Anwendung:
Die Webcam wird im Hintergrund gestartet.
DeepFace erkennt automatisch die dominierende Emotion deines Gesichts (z. B. „happy“, „sad“, „angry“ etc.).
In der GUI klickst du auf „Jetzt analysieren“.
---
Die Anwendung:
liest die aktuelle Emotion
sucht einen passenden Song aus einer vorbereiteten Liste
fragt bei Spotify per API nach Details zum Song
zeigt dir Songtitel, Künstler und Dauer in einem Infofenster an
---

