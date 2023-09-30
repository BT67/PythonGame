import socket
import json
import datetime
import random
import threading

IP = "127.0.0.1"
PORT = 8081
MAX_CLIENTS = 10
PACKET_SIZE = 2048
MAP = {}



def timeNow():
    return str(datetime.datetime.now()) + " "


def assign_client_id(clients: dict, max_clients: int):
    while True:
        client_id = str(random.randint(1, max_clients))
        if client_id not in clients:
            return client_id


def handle_packet(client_id: str):
    client_info = clients[client_id]
    connection: socket.socket = client_info["socket"]
    while True:
        try:
            packet = connection.recv(PACKET_SIZE)
        except:
            break
        if not packet:
            break
        packet_data = packet.decode("utf8")
        try:
            packet_start_index = packet_data.index("{")
            packet_end_index = packet_data.index("}") + 1
            packet_data = packet_data[packet_start_index:packet_end_index]
            packet_data = json.loads(packet_data)
            print(timeNow() + f"packet from clientID={client_id}, packet data={str(packet_data)}")
            return packet_data
        except Exception as e:
            print(e)


clients = {}

# Initiate server socket:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(MAX_CLIENTS)
print(timeNow() + "server initialisation completed, server host=" + IP)

# def update_battle():


def main():
    while True:
        # Listen for new connection and assign client ID:
        connection, address = server_socket.accept()
        client_id = assign_client_id(clients, MAX_CLIENTS)
        connection.send(client_id.encode("utf8"))
        print(timeNow() + "client connected, clientID=" + client_id)

if __name__ == "__main__":
    main()
