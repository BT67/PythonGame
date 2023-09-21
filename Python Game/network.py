import socket
import json
import datetime
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081


def timeNow():
    return str(datetime.datetime.now()) + " "


class Network:

    def __init__(self, server_ip: str, server_port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.packet_size = 2048
        self.id = 0

    def set_timeout(self, timeout):
        self.client.settimeout(timeout)

    def connect(self):
        self.client.connect((self.server_ip, self.server_port))
        self.id = self.client.recv(self.packet_size).decode("utf8")
        print(timeNow() + "server connection established")

    def handle_packet(self):
        packet = 0
        try:
            packet = self.client.recv(self.packet_size)
        except socket.error as e:
            print(e)
        if not packet:
            return None
        packet_data = packet.decode("utf8")
        try:
            packet_start_index = packet_data.index("{")
            packet_end_index = packet_data.index("}") + 1
            packet_data = packet_data[packet_start_index:packet_end_index]
            packet_data = json.loads(packet_data)
        except Exception as e:
            print(e)
        return packet_data


