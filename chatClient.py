import sys
from socket import *
import threading


class chat_client:
    END_CONVO = "Bye"  # Used to end the chat

    def __init__(self):

        self.SERVER_ADDR = '127.0.0.1'
        self.SERVER_PORT = 12013
        self.end_chat = False

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.client_socket.connect((self.SERVER_ADDR, self.SERVER_PORT))
        except socket.error as e:
            print(str(e))

    def recv_msg(self):
        """
        Used to receive messages from server
        """
        while not self.end_chat:
            msg = self.client_socket.recv(1024).decode()
            if msg == self.END_CONVO:
                self.end_chat = True
            elif msg:
                print(msg)

    def send_msg(self):
        """
        Prompts user for message
        """
        while True:
            msg = input("")
            self.client_socket.send(msg.encode())

    def launch_client(self):
        """
        Creates threads for messaging and listens for msgs
        """
        thread = threading.Thread(target=self.send_msg, daemon=True)
        thread.start()
        # receives messages from server
        self.recv_msg()
        # closes close whence done
        print("[CLIENT] DISCONNECTING")
        self.client_socket.close()
        print("[CLIENT] DISCONNECTED. Byeeee")


if __name__ == "__main__":
    print("[CLIENT] Starting chat client")
    app = chat_client()
    app.launch_client()
