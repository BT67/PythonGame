import socket
import threading
import datetime
from math import radians

import psycopg2
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from network import Network
from main_menu import MainMenu

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081

TURN_SPEED = 0.25
ZOOM_SPEED = 0.5
MAX_ZOOM_IN = 0
MAX_ZOOM_OUT = -10
MOVE_SPEED_ACC = 0.016
MOVE_SPEED_DECC = 0.015
MAX_SPEED = 0.035
MAX_LOOK_UP = 45

app = Ursina()

Sky()

window.fps_counter.enabled = False


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


def main():
    packet_thread = threading.Thread(target=listen, daemon=True)
    packet_thread.start()
    app.run()


def update():
    player_camera.rotation_y = player_camera.rotation_y % 360
    player_model.rotation_y = player_model.rotation_y % 360
    if camera.rotation_x > MAX_LOOK_UP:
        camera.rotation_x = MAX_LOOK_UP
    player_camera.y = player_model.y
    move_speed = player_model.move_speed
    move_speed -= MOVE_SPEED_DECC
    move_direction = player_model.rotation_y
    if move_speed <= 0:
        move_speed = 0
        player_model.reverse = 0
    if held_keys['w'] | held_keys['up arrow']:
        move_speed += MOVE_SPEED_ACC
        player_model.reverse = 0
    if held_keys['a'] | held_keys['left arrow']:
        if player_model.reverse:
            player_model.pivot_y = - 3
            player_model.rotation_y += TURN_SPEED
        else:
            player_model.pivot_y = 3
            player_model.rotation_y -= TURN_SPEED
    if held_keys['s'] | held_keys['down arrow']:
        player_model.reverse = 1
        move_speed += MOVE_SPEED_ACC
    if held_keys['d'] | held_keys['right arrow']:
        if player_model.reverse:
            player_model.pivot_y = 3
            player_model.rotation_y -= TURN_SPEED
        else:
            player_model.pivot_y = - 3
            player_model.rotation_y += TURN_SPEED
    if move_speed > MAX_SPEED:
        move_speed = MAX_SPEED
    if player_model.reverse:
        move_direction = 180 + player_model.rotation_y
    #player_model.z += cos(radians(move_direction)) * move_speed
    #player_model.x += sin(radians(move_direction)) * move_speed
    player_camera.z = player_model.z
    player_camera.x = player_model.x
    player_model.move_speed = move_speed

def input(key):
    if key == Keys.scroll_up:
        camera.z += ZOOM_SPEED
        if camera.z > MAX_ZOOM_IN:
            camera.z = MAX_ZOOM_IN
    if key == Keys.scroll_down:
        camera.z -= ZOOM_SPEED
        if camera.z < MAX_ZOOM_OUT:
            camera.z = MAX_ZOOM_OUT


ground = Entity(
    model="plane",
    scale=(100, 1, 100),
    position=(0, 0, 0),
    color=color.light_gray,
    texture="white_cube",
    texture_scale=(100, 100),
    collider="box"
)

player_camera = FirstPersonController(
    origin_y=-0.5,
    model="cube",
    collider="box",
    visible=False,
    speed=1
)

# z=8,
player_model = Entity(
    model="tier1.fbx",
    y=0.01,
    scale=(0.005, 0.005, 0.005),
    color=color.dark_gray,
    collider="box",
    texture="white_cube"
)

player_model.move_speed = 0
player_model.reverse = 0

#camera.z = -5

main_menu = MainMenu(LANGUAGE="english", THEME="default")
player_model.enabled = False
player_camera.enabled = False

connection = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="postgres",
    password="root"
)

if __name__ == "__main__":
    main()
