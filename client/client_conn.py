"""
TCP connection to HOST (localhost:2106)
receive commands from host to start, stop running
send data
    isRunning
    isTracking
    faceData
"""
import socket
from src.DetectEmotion import predict
import threading


HOST = '127.0.0.1'  
PORT = 12345       
class Client:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 12345
        self.__connect()
        self.isUp = False
        self.isActive = False
        self.emotion_recognizer = predict.EmotionRecognizer()

    def __connect(self):
        self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__conn.connect((self.__HOST, self.__PORT))
        self.isUp = True
    
    def handle_commands(self):
        command = self.__conn.recv(1024).decode()
        print(f"Command Received: {command}")
        if command == "start":
            self.__conn.send("starting".encode())
            self.start_emotion_detection()

        elif command == "status":
            response = f"Status: {self.isUp}, Active: {self.isActive}"
            self.send_response(response)

    def start_emotion_detection(self):
        self.isActive = True
        emotion_thread = threading.Thread(target=self.emotion_recognizer.run_emotion_detection)
        emotion_thread.start()

    def send_response(self, response):
        self.__conn.send(response.encode())
    
    def start_emotion_detection(self):
        self.isActive = True
        emotion_thread = threading.Thread(target=self.emotion_recognizer.run_emotion_detection)
        emotion_thread.start()

    def send_emotion(self):
        while True:
            with self.emotion_recognizer.emotion_lock:
                if self.emotion_recognizer.emotion:
                    self.send_response(self.emotion_recognizer.emotion)

    # def handle_commands(self):
    #     command = self.__conn.recv(1024).decode()
    #     print(f"Command Received: {command}")
    #     if command == "start":
    #         self.__conn.send("starting".encode())
    #         while True:
    #             self.isActive = True
    #             emotion_gen = videoTester.detect_emotion()
    #             for e in emotion_gen:
    #                 self.send_response(e)
        
    #     elif command == "status":
    #         response = f"Status: {self.isUp}, Active: {self.isActive}"
    #         self.send_response(response)
    
    def __process_emotion(self):
        emotion_gen = videoTester.detect_emotion()
        for e in emotion_gen:
            self.send_response(e)
    
    def close_conn(self):
        self.isActive, self.isUp = False, False
        self.__conn.close()

    def checkUp(self):
        return self.isUp

    def checkActive(self):
        return self.isActive


if __name__ == "__main__":
    recognizer = Client()
    emotion_sender_thread = threading.Thread(target=recognizer.send_emotion)
    emotion_sender_thread.start()

    while True:
        recognizer.handle_commands()

