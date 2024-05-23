import cv2
import mediapipe as mp
import numpy as np
import os

# Инициализация распознавания лиц
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Путь к папке с фотографиями
dataset_dir = 'data'
user_id = 1  # ID для вашего лица


def get_images_and_labels(dataset_dir):
    image_paths = [os.path.join(root, file)
                   for root, dirs, files in os.walk(dataset_dir)
                   for file in files if file.endswith('jpg')]
    face_samples = []
    ids = []

    for image_path in image_paths:
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        face_id = int(os.path.basename(os.path.dirname(image_path)))
        faces = face_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            face_samples.append(gray[y:y + h, x:x + w])
            ids.append(face_id)

    return face_samples, ids


# Обучение модели, если есть данные для обучения
if os.path.exists(dataset_dir):
    faces, ids = get_images_and_labels(dataset_dir)
    if faces and ids:
        recognizer.train(faces, np.array(ids))
        recognizer.save('trainer.yml')
        recognizer.read('trainer.yml')

# Инициализация распознавания рук
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Ваши имя и фамилия
first_name = "Stepan"
last_name = "Tischenko"


def count_fingers(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    for i in range(1, 5):
        if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)


# Захват видео с веб-камеры
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    hand_label = ""
    show_name = False
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_count = count_fingers(hand_landmarks)
            if user_id in ids:  # Пользователь есть в базе
                if fingers_count == 1:
                    hand_label = first_name
                elif fingers_count == 2:
                    hand_label = last_name
                elif fingers_count == 3:
                    hand_label = f"{first_name} {last_name}"
                show_name = True

    for (x, y, w, h) in faces:
        face_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence < 60:  # Уровень доверия ниже 100 означает совпадение
            if face_id == user_id:  # Пользователь есть в базе
                if show_name:
                    cv2.putText(frame, hand_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        else:  # Пользователь отсутствует в базе
            cv2.putText(frame, "unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
