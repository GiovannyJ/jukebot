import socket
import threading
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image

class EmotionRecognizer:
    def __init__(self, model_path='fer.json', weights_path='fer.h5', cascade_path='haarcascade_frontalface_default.xml'):
        self.model = model_from_json(open(model_path, "r").read())
        self.model.load_weights(weights_path)
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.emotion = None
        self.emotion_lock = threading.Lock()

    def predict_emotion(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = self.face_cascade.detectMultiScale(gray_img, 1.32, 5)

        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

        for (x, y, w, h) in faces_detected:
            roi_gray = gray_img[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255

            predictions = self.model.predict(img_pixels)
            max_index = np.argmax(predictions[0])
            predicted_emotion = emotions[max_index]

            with self.emotion_lock:
                self.emotion = predicted_emotion

    def run_emotion_detection(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, test_img = cap.read()
            if not ret:
                continue

            self.predict_emotion(test_img)
            
            # Overlay detected emotion on the video feed
            with self.emotion_lock:
                if self.emotion:
                    cv2.putText(test_img, f'Emotion: {self.emotion}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the video feed
            cv2.imshow("Emotion Detection", test_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recognizer = EmotionRecognizer()
    emotion_detection_thread = threading.Thread(target=recognizer.run_emotion_detection)
    emotion_detection_thread.start()

    emotion_detection_thread.join()  # Wait for the emotion detection thread to finish

    cv2.destroyAllWindows()  # Close the OpenCV window when done
