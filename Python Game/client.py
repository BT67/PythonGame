import socket
import threading
import datetime
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from network import Network

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081

CAMERA_SPEED = 0.2
ZOOM_SPEED = 0.5

app = Ursina()

Sky()


def timeNow():
    return str(datetime.datetime.now()) + " "


# Main server connection loop:
while True:
    network = Network(SERVER_HOST, SERVER_PORT)
    network.set_timeout(10)
    error_occurred = False
    try:
        network.connect()
    except ConnectionRefusedError:
        print(timeNow() + "unable to connect to host server")
        error_occurred = True
    except socket.timeout:
        print(timeNow() + "server connection timed out")
        error_occurred = True
    except socket.gaierror:
        print(timeNow() + "unable to connect to host server")
        error_occurred = True
    finally:
        network.set_timeout(None)
    if not error_occurred:
        break


def listen():
    while True:
        try:
            info = network.handle_packet()
        except Exception as e:
            print(e)
            continue
        if not info:
            continue


def update():
    print()


def main():
    packet_thread = threading.Thread(target=listen, daemon=True)
    packet_thread.start()
    game_thread = threading.Thread(target=update, daemon=True)
    game_thread.start()
    app.run()


player = FirstPersonController(model='cube', color=color.orange, y=2, origin_y=-.5, speed=8, collider='box')

ground = Entity(
    model="plane",
    scale=(100, 1, 100),
    color=color.gray,
    texture="white_cube",
    texture_scale=(100, 100),
    collider="box"
)

if __name__ == "__main__":
    main()
