import cv2
from deepface import DeepFace

# Kamera starten
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Gesichter extrahieren
        faces = DeepFace.extract_faces(frame, enforce_detection=False)
        for face in faces:
            region = face["facial_area"]
            x, y, w, h = region["x"], region["y"], region["w"], region["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    except Exception as e:
        print("Fehler bei der Gesichtserkennung:", e)

    cv2.imshow("Gesichtserkennung mit DeepFace", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
