import socket
import json
import datetime
import random
import threading

import psycopg2
from ursina import *

IP = "127.0.0.1"
PORT = 8081
MAX_CLIENTS = 10
PACKET_SIZE = 2048
maps = []
clients = {}
lobby = []


def process_register(client_id, username, password, email):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="root"
    )
    query = """INSERT INTO public.python_users(username, password, email, online_status, current_client, in_battle) VALUES(%s,%s,%s,false,%s,false);"""
    values = [
        username,
        password,
        email,
        client_id
    ]
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        packet = {
            "type": "REGISTER_STATUS",
            "status": True
        }
        clients[client_id].send(json.dumps(packet).encode("utf-8"))
    except psycopg2.Error as e:
        print(e)
        packet = {
            "type": "REGISTER_STATUS",
            "status": False
        }
        clients[client_id].send(json.dumps(packet).encode("utf-8"))
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
    except psycopg2.Error as e:
        print(e)
    if row is not None and len(row) > 0:
        try:
            query = """UPDATE public.python_users SET online_status = true, current_client = %s WHERE username = %s AND password = %s AND online_status = false;"""
            values = [
                int(client_id),
                username,
                password
            ]
            cursor.execute(query, values)
            packet = {
                "type": "LOGIN_STATUS",
                "status": True
            }
            clients[client_id].send(json.dumps(packet).encode("utf-8"))
        except psycopg2.Error as e:
            print(e)
            packet = {
                "type": "LOGIN_STATUS",
                "status": False
            }
            clients[client_id].send(json.dumps(packet).encode("utf-8"))
    else:
        packet = {
            "type": "LOGIN_STATUS",
            "status": False
        }
        clients[client_id].send(json.dumps(packet).encode("utf-8"))
    connection.commit()
    cursor.close()
    connection.close()


def process_logout(client_id):
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="root"
    )
    cursor = connection.cursor()
    try:
        query = """UPDATE public.python_users SET online_status = false, current_client = NULL WHERE current_client = %s AND online_status = true;"""
        values = [
            int(client_id),
        ]
        cursor.execute(query, values)
    except psycopg2.Error as e:
        print(e)
    connection.commit()
    cursor.close()
    connection.close()


def process_enter_lobby(client_id):
    lobby.append(client_id)


def process_leave_lobby(client_id):
    lobby.pop(lobby.index(client_id))


def timenow():
    return str(datetime.datetime.now()) + " "


def assign_client_id(clients: dict, max_clients: int):
    while True:
        client_id = str(random.randint(1, max_clients))
        if client_id not in clients:
            return client_id


def handle_packet(client_id: str):
    connection = clients[client_id]
    while True:
        try:
            packet = connection.recv(PACKET_SIZE)
        except Exception as e:
            print(timenow() + str(e))
            break
        if not packet:
            break
        packet_data = packet.decode("utf8")
        try:
            # packet_start_index = packet_data.index("{")
            # packet_end_index = packet_data.index("}") + 1
            # packet_data = packet_data[packet_start_index:packet_end_index]
            packet_data = json.loads(packet_data)
            print(timenow() + "packet from clientID={client_id}, packet data=" + str(packet_data))
            match packet_data["type"]:
                case "REGISTER":
                    process_register(packet_data["client_id"], packet_data["username"], packet_data["password"],
                                     packet_data["email"])
                    break
                case "LOGIN":
                    process_login(packet_data["client_id"], packet_data["username"], packet_data["password"])
                case "LOGOUT":
                    process_logout(packet_data["client_id"])
                case "ENTER_LOBBY":
                    process_enter_lobby(packet_data["client_id"])
                    check_lobby(packet_data["client_id"])
                case "LEAVE_LOBBY":
                    process_leave_lobby(packet_data["client_id"])
        except Exception as e:
            print(e)


# Initiate server socket:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(MAX_CLIENTS)
print(timenow() + "server initialisation completed, server host=" + IP)


def listen():
    while True:
        try:
            handle_packet()
        except Exception as e:
            print(e)
            continue


def check_lobby(client_id):
    servers_full = True
    for map_obj in maps:
        if not map_obj["is_full"]:
            servers_full = False
            packet = {
                "type": "ENTER_MAP",
                "map_name": map_obj["map_name"]
            }
            clients[client_id].send(json.dumps(packet).encode("utf-8"))
            print(timenow() + "moving clientID=" + client_id + " into map=" + map_obj["map_name"])
            lobby.pop(lobby.index(client_id))
    if servers_full:
        packet = {
            "type": "SERVERS_FULL",
        }
        clients[client_id].send(json.dumps(packet).encode("utf-8"))


def maps_update_loop():
    for map_obj in maps:
        for client in map_obj["clients"]:
            # Send client positions of all clients in the map, including itself
            for otherClient in map_obj.clients:
                packet = {
                    "type": "POS",
                    "entity_name": otherClient.entity_name
                }
                clients[client.client_id].send(json.dumps(packet).encode("utf-8"))


def main():
    # Set all users online_status = false
    connection = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="root"
    )
    cursor = connection.cursor()
    try:
        query = """UPDATE public.python_users SET online_status = false, current_client = NULL;"""
        cursor.execute(query)
    except psycopg2.Error as e:
        print(e)
    connection.commit()
    cursor.close()
    connection.close()
    # Init Maps:
    new_map = {
        "map_name": "map1",
        "clients": {},
        "size": 1000,
        "ground": {
            "texture": "white_cube",
            "color": color.light_gray
        },
        "is_full": False
    }
    maps.append(new_map)
    # Start maps update thread:
    maps_thread = threading.Thread(target=maps_update_loop, daemon=True)
    maps_thread.start()
    while True:
        # Listen for new connection and assign client ID:
        connection, address = server_socket.accept()
        client_id = assign_client_id(clients, MAX_CLIENTS)
        clients[client_id] = connection
        connection.send(client_id.encode("utf8"))
        print(timenow() + "client connected, clientID=" + client_id)
        print(timenow() + str(connection))
        try:
            handle_packet(client_id)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
