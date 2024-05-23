import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

user_id = 1  # Уникальный ID для вашего лица
dataset_dir = 'data'
user_dir = os.path.join(dataset_dir, str(user_id))

if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

sample_count = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        sample_count += 1
        cv2.imwrite(f'{user_dir}/{sample_count}.jpg', gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or sample_count >= 100:
        break

cap.release()
cv2.destroyAllWindows()
