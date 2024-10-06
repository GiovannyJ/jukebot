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

class Host:
    def __init__(self):
        self.__HOST = '127.0.0.1'#'192.168.1.215'
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

        try:
            while True:
                self.__client, addr = self.__server.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")
                self.__handle_client()

        except KeyboardInterrupt:
            print("Ctrl+C detected. Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.__server.close()

    def __handle_client(self):
        command = input("Enter a command: ")
        self.__client.send(command.encode())
        
        response = self.__client.recv(1024).decode()
        if response in self.emotion_count:
            self.__process_response(response)

    def __process_response(self, response):
        self.emotion_count[response] += 1

        if self.emotion_count['angry'] == 5:
            pass
        
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

