import cv2
from deepface import DeepFace

# Kamera starten
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Gesichter + Emotion analysieren
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)

        # Wenn mehrere Gesichter erkannt wurden
        if isinstance(result, list):
            faces = result
        else:
            faces = [result]

        for face in faces:
            region = face["region"]
            emotion = face["dominant_emotion"]

            # Nur anzeigen, wenn Emotion "happy" oder "sad"
            if emotion in ["happy", "sad"]:
                x, y, w, h = region["x"], region["y"], region["w"], region["h"]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    except Exception as e:
        print("Fehler bei der Analyse:", e)

    cv2.imshow("Gesicht + Emotion (happy/sad)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
