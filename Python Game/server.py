import socket
import json
import datetime
import random

import psycopg2

IP = "127.0.0.1"
PORT = 8081
MAX_CLIENTS = 10
PACKET_SIZE = 2048
MAP = {}


def process_register(client_id, username, password, email):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="root"
    )
    query = """INSERT INTO public.python_users(username, password, email, online_status, current_client) VALUES(%s,%s,%s,false,null);"""
    values = [
        username,
        password,
        email,
    ]
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
    except psycopg2.Error:
        clients[client_id].send([
            "REGISTER_STATUS",
            False
        ])
    connection.commit()
    cursor.close()
    connection.close()

def process_login(client_id, username, password):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="root"
    )
    row = []
    cursor = connection.cursor()
    try:
        query = """SELECT * from public.python_users WHERE username = %s AND password = %s AND online_status = false;"""
        values = [
            username,
            password
        ]
        cursor.execute(query, values)
        row = cursor.fetchone()
    except psycopg2.Error:
        # TODO add server log msg
        print()
    cursor.close()
    connection.close()
    if row is not None and len(row) > 0:
        try:
            query = """UPDATE public.python_users SET online_status = true, current_client = %s WHERE username = %s AND password = %s AND online_status = false;"""
            values = [
                client_id,
                username,
                password
            ]
            cursor.execute(query, values)
            clients[client_id].send([
                "LOGIN_STATUS",
                True
            ])
        except psycopg2.Error:
            clients[client_id].send([
                "LOGIN_STATUS",
                False
            ])
    else:
        clients[client_id].send([
            "LOGIN_STATUS",
            False
        ])
    cursor.close()
    connection.close()


def timenow():
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
            print(timenow() + f"packet from clientID={client_id}, packet data={str(packet_data)}")
            match packet_data.packet_type:
                case "REGISTER":
                    process_register(packet_data.username, packet_data.password, packet_data.email)
                case "LOGIN":
                    process_login(packet_data.username, packet_data.password)
        except Exception as e:
            print(e)


clients = {}

# Initiate server socket:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(MAX_CLIENTS)
print(timenow() + "server initialisation completed, server host=" + IP)


# def update_battle():


def main():
    while True:
        # Listen for new connection and assign client ID:
        connection, address = server_socket.accept()
        client_id = assign_client_id(clients, MAX_CLIENTS)
        connection.send(client_id.encode("utf8"))
        print(timenow() + "client connected, clientID=" + client_id)


if __name__ == "__main__":
    main()
