import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

dataset_dir = r'data'


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


faces, ids = get_images_and_labels(dataset_dir)
recognizer.train(faces, np.array(ids))
recognizer.save('trainer.yml')
