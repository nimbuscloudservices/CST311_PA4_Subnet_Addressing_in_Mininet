import sys
import socket
import threading


class chat_client:
    END_CONVO = "Bye"  # Used to end the chat

    def __init__(self):

        self.SERVER_ADDR = "127.0.0.1"
        self.SERVER_PORT = 12013
        self.ADDR = (self.SERVER_ADDR, self.SERVER_PORT)
        self.end_chat = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recv_msg(self):
        """
        Used to receive messages from server
        """
        while not self.end_chat:
            msg = self.client_socket.recv(1024).decode()
            if msg.lower() == self.END_CONVO.lower():
                self.end_chat = True
                break
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
        # connects to server
        try:
            print("Connecting to chat server: {0}:{1}...".format(self.ADDR[0], self.ADDR[1]))
            self.client_socket.connect(self.ADDR)
        except socket.error as e:
            print("An error occurred, {}".format(str(e)))
            print("Try again with correct server address and port")
            sys.exit(1)

        print("Connected to {0}:{1}".format(self.ADDR[0], self.ADDR[0]))

        # sends messages to server
        send_thread = threading.Thread(target=self.send_msg, daemon=True)
        send_thread.start()

        self.recv_msg()
        # closes client whence done
        self.client_socket.close()
        sys.exit(0)



if __name__ == "__main__":
    print("Starting chat client...")
    app = chat_client()
    app.launch_client()
    sys.exit(0)
