"""
Team Programming Assignment 3


"""

import socket
import threading


class chatServer:
    """
        Class for chat server
        """
    CLIENT_NAMES = ["X", "Y"]  # Names for clients
    ORDER = {1: "first", 2: "second"}  # ordering
    MAX_CLIENTS = 2  # maximum clients supported
    END_CONVO_KEYWORD = "Bye"

    def __init__(self):
        self.SERVER_ADDR = "127.0.0.1"
        self.SERVER_PORT = 12013
        self.ADDR = (self.SERVER_ADDR, self.SERVER_PORT)
        self.connections = []  # holds active connections
        self.received_msgs = []  # holds messages from clients
        self.client_threads = []  # holds active threads
        self.end_chat = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection_handler(self):
        """
        Handles connection to clients and assigning order
        """
        self.server.listen(2)

        print("The server is waiting to receive two connections...\n")
        while len(self.connections) < self.MAX_CLIENTS:
            conn, addr = self.server.accept()
            self.connections.append(conn)
            index = self.connections.index(conn)
            print("Accepted {0} connection, calling it {1}".format(self.ORDER[index + 1], self.CLIENT_NAMES[index]))

        print("\n")

    def send_confirmation(self, client_list):
        """
        Sends confirmation to connected clients in client_list
        :param client_list: list of active clients
        """
        for client in client_list:
            index = client_list.index(client)
            msg = "From Server: Client {} connected.".format(self.CLIENT_NAMES[index])
            client.send(msg.encode())

    def recv_msg(self, conn):
        """
        used to receive messages from clients, decode, and format
        :param conn: connection socket object
        """

        name = self.connections.index(conn)
        # infinite loop to accept and decode messages
        while not self.end_chat:
            msg = conn.recv(1024).decode()
            #  Listens for end_convo_keyword
            if msg:
                self.broadcast(msg, self.CLIENT_NAMES[name])
                if msg == self.END_CONVO_KEYWORD:
                    self.end_chat = True

    def broadcast(self, msg, name="[SERVER]"):
        """
        broadcast message to all clients
        """
        mod_msg = "{0}: {1}".format(name, msg)
        print(mod_msg)
        for client in self.connections:
            client.send(mod_msg.encode())

    def start_client_communications(self):
        """
        Starts threads for clients in connection array to receive messages from them.
        """
        for client in self.connections:
            thread = threading.Thread(target=self.recv_msg, args=(client,))
            self.client_threads.append(thread)
            thread.start()

    def end_connections(self):
        """
        Joins threads and terminates connections
        """
        goodbye_msg = "[SERVER] Terminated your connection"
        for client in self.connections:
            client.send(goodbye_msg.encode())
            client.send(self.END_CONVO_KEYWORD.encode())
        for thread in self.client_threads:
            thread.join()
        for client in self.connections:
            client.close()

    def launch_server(self):
        """
        launches the server
        """
        print("[STARTING] Server is starting...")
        try:
            self.server.bind(self.ADDR)
        except socket.error as e:
            print(str(e))
        # starts accepting client connections
        self.connection_handler()
        # sends confirmations to both clients with their names
        self.send_confirmation(self.connections)

        print("[SERVER] Waiting to receive messages from client X and client Y...")

        self.start_client_communications()
        while not self.end_chat:
            pass
        # tells clients whose message was received first

        print("[SERVER] Waiting for clients to close connections...")
        # terminates
        self.end_connections()

        print("[SERVER] Connections successfully terminated.")


if __name__ == "__main__":
    chatapp = chatServer()
    chatapp.launch_server()
