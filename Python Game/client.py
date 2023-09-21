import socket
import threading
import datetime
from player import Player
from ursina import *
from network import Network

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081

CAMERA_SPEED = 0.2
ZOOM_SPEED = 0.5

app = Ursina()

entities = {}
indicators = {}


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
    if held_keys['w'] | held_keys['up arrow']:
        camera.y += CAMERA_SPEED
    if held_keys['a'] | held_keys['left arrow']:
        camera.x -= CAMERA_SPEED
    if held_keys['s'] | held_keys['down arrow']:
        camera.y -= CAMERA_SPEED
    if held_keys['d'] | held_keys['right arrow']:
        camera.x += CAMERA_SPEED
    for entity in entities:
        if entities[entity].focused:
            indicators["test_selection_indicator"].visible = True
        else:
            indicators["test_selection_indicator"].visible = False


def input(key):
    if key == Keys.scroll_up:
        camera.z += ZOOM_SPEED
        camera.y += ZOOM_SPEED
    if key == Keys.scroll_down:
        camera.z -= ZOOM_SPEED
        camera.y -= ZOOM_SPEED
    if key == Keys.left_mouse_down and not mouse.hovered_entity:
        for entity in entities:
            entities[entity].set_unfocused()



def main():
    packet_thread = threading.Thread(target=listen, daemon=True)
    packet_thread.start()
    game_thread = threading.Thread(target=update, daemon=True)
    game_thread.start()
    app.run()


test_entity = Player()
test_entity.model = "cube"
test_entity.position = (0, 0, 0)
test_entity.color = color.light_gray
test_entity.texture = "white_cube"
test_entity.collider = "box"
test_entity.name = "test"

selection_indicator = Entity(
    model="sphere",
    scale=(0.5, 0.5, 0.5),
    position=(0, 0, 2),
    color=color.green,
    name="test_selection_indicator",
    visible=False
)

entities.update({test_entity.name: test_entity})
indicators.update({selection_indicator.name: selection_indicator})

camera.rotation_x = -30

if __name__ == "__main__":
    main()
