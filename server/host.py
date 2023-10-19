'''
Using TCP connection (localhost:2106)
-send commands to JukeBot
    start running
    stop running
    pause running
-receive data from Jukebot
    face data
    isRunning -> if no then pause music
    isTracking -> if no then pause music
'''

import socket
from src import spotify_controller

# HOST = '127.0.0.1'
# PORT = 12345

# sc = spotify_controller.spotify()

# emotion_count = {
#     'angry': 0,
#     'disgust': 0,
#     'fear': 0,
#     'happy': 0,
#     'sad': 0,
#     'surprise': 0,
#     'neutral': 0,
# }
# def handle_client(client_socket):
#     command = input("Enter a command: ")

#     client_socket.send(command.encode())
#     while True:

#         response = client_socket.recv(1024).decode()
#         print(f"Client response: {response}")
        
#         if response in emotion_count:
#             process_response(response)

# def process_response(response):
#     # Update the response count for the received response
#     emotion_count[response] += 1

#     if emotion_count['angry'] == 5:
#         print("THATS ONE ANGRY NIGGER")
    
#     elif emotion_count['disgust'] == 5:
#         self.__sc.play_song("HUMBLE")
    
#     elif emotion_count['fear'] == 5:
#         pass
    
#     elif emotion_count['happy'] == 5:
#         self.__sc.play_song("HUMBLE")
    
#     elif emotion_count['sad'] == 5:
#         pass
    
#     elif emotion_count['surprise'] == 5:
#         pass
    
#     elif emotion_count['neutral'] == 5:
#         pass


# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((HOST, PORT))
#     server.listen(5)

#     print(f"Listening on {HOST}:{PORT}")

#     while True:
#         client_socket, addr = server.accept()
#         print(f"Accepted connection from {addr[0]}:{addr[1]}")

#         handle_client(client_socket)

class Host:
    def __init__(self):
        self.__HOST = '127.0.0.1'
        self.__PORT = 12345
        self.__sc = spotify_controller.spotify()
        self.emotion_count = {
                'angry': 0,
                'disgust': 0,
                'fear': 0,
                'happy': 0,
                'sad': 0,
                'surprise': 0,
                'neutral': 0,
            }

    def StartServer(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__HOST, self.__PORT))
        self.__server.listen(5)
        print(f"Listening on {self.__HOST}:{self.__PORT}")

        while True:
            self.__client, addr = self.__server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            self.__handle_client()

    def __handle_client(self):
        command = input("Enter a command: ")
        self.__client.send(command.encode())
        
        response = self.__client.recv(1024).decode()
        if response in self.emotion_count:
            self.__process_response(response)

    def __process_response(self, response):
        self.emotion_count[response] += 1

        if self.emotion_count['angry'] == 5:
            print("THATS ONE ANGRY NIGGER")
        
        elif self.emotion_count['disgust'] == 5:
            self.__sc.play_song("HUMBLE")
        
        elif self.emotion_count['fear'] == 5:
            self.__sc.play_song("WESPN")
        
        elif self.emotion_count['happy'] == 5:
            self.__sc.play_song("Hellcat Kenny")
        
        elif self.emotion_count['sad'] == 5:
            self.__sc.play_song("passionfruit")
        
        elif self.emotion_count['surprise'] == 5:
            self.__sc.play_song("We Major")
        
        elif self.emotion_count['neutral'] == 5:
            self.__sc.play_song("N side")

def main():
    h = Host()
    h.StartServer()

if __name__ == '__main__':
    main()

