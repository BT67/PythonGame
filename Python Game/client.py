import socket
import json
import datetime
import threading
from math import radians
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from lang_config import lang_config
from themes_config import themes
from maps_ref import map_models

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
LANGUAGE = "english"
THEME = "default"

app = Ursina()

Sky()

window.fps_counter.enabled = False

# Server Connection:

PACKET_SIZE = 2048
client_id = 0


def handle_packet():
    packet = 0
    try:
        packet = network.recv(PACKET_SIZE)
    except socket.error as e:
        print(e)
    if not packet:
        return None
    packet_data = packet.decode("utf8")
    try:
        # packet_start_index = packet_data.index("{")
        # packet_end_index = packet_data.index("}") + 1
        # packet_data = packet_data[packet_start_index:packet_end_index]
        packet_data = json.loads(packet_data)
        match packet_data["type"]:
            case "REGISTER_STATUS":
                register_status(packet_data["status"])
            case "LOGIN_STATUS":
                login_status(packet_data["status"])
            case "SERVERS_FULL":
                lbl_lobby.text = lang_config[LANGUAGE]["servers_full"]
            case "ENTER_MAP":
                enter_map(packet_data["map_name"])
            case "POS":
                update_pos(
                    packet_data["entity_name"]
                )

    except Exception as e:
        print(e)


# Menus:

# Initialise menus:
menus_entity = Entity(parent=camera.ui)
init_menu = Entity(parent=menus_entity, enabled=True)
login_menu = Entity(parent=menus_entity, enabled=False)
register_menu = Entity(parent=menus_entity, enabled=False)
register_success_menu = Entity(parent=menus_entity, enabled=False)
main_menu = Entity(parent=menus_entity, enabled=False)
lobby_menu = Entity(parent=menus_entity, enabled=False)
in_game_menu = Entity(parent=menus_entity, enabled=False)
settings_menu = Entity(parent=menus_entity, enabled=False)
video_menu = Entity(parent=menus_entity, enabled=False)
gameplay_menu = Entity(parent=menus_entity, enabled=False)
audio_menu = Entity(parent=menus_entity, enabled=False)
controls_menu = Entity(parent=menus_entity, enabled=False)
pause_menu = Entity(parent=menus_entity, enabled=False)
quit_menu = Entity(parent=menus_entity, enabled=False)

menus = [
    init_menu,
    login_menu,
    register_menu,
    main_menu,
    lobby_menu,
    settings_menu,
    video_menu,
    gameplay_menu,
    audio_menu,
    controls_menu,
    pause_menu,
    quit_menu,
]

# UI audio
click = Audio("click.wav", False, False, volume=10)


# Init Menu Buttons

def btn_login_init_event():
    lbl_login_msg.text = ""
    login_menu.enabled = True
    init_menu.enabled = False


btn_login_init = Button(
    text=lang_config[LANGUAGE]["login"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=init_menu,
    x=-0.15,
    y=-0.1,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_login_init.on_click = btn_login_init_event


def btn_register_init_event():
    register_menu.enabled = True
    init_menu.enabled = False


btn_register_init = Button(
    text=lang_config[LANGUAGE]["register"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=init_menu,
    x=0.15,
    y=-0.1,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_register_init.on_click = btn_register_init_event


def btn_quit_event():
    quit()


def btn_back_event():
    if login_menu.enabled:
        init_menu.enabled = True
        login_menu.enabled = False
    if register_menu.enabled:
        init_menu.enabled = True
        register_menu.enabled = False
    if register_success_menu.enabled:
        init_menu.enabled = True
        register_success_menu.enabled = False


btn_quit_init = Button(
    text=lang_config[LANGUAGE]["quit"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=init_menu,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_quit_init.on_click = btn_quit_event

# Login Menu

login_menu_back = Entity(
    model="cube",
    color=themes[THEME]["ui_background"],
    scale_x=0.6,
    scale_y=0.5,
    position_z=1,
    parent=login_menu
)

lbl_login_msg = Text(
    text="",
    x=-0.25,
    parent=login_menu
)

lbl_username_login = Text(
    text=lang_config[LANGUAGE]["username"],
    x=-0.25,
    y=0.2,
    parent=login_menu
)

lbl_password_login = Text(
    text=lang_config[LANGUAGE]["password"],
    x=-0.25,
    y=0.1,
    parent=login_menu
)

txt_username_login = InputField(
    color=color.black,
    y=0.15,
    parent=login_menu
)

txt_password_login = InputField(
    color=color.black,
    y=0.05,
    hide_content=True,
    parent=login_menu
)

txt_username_login.next_field = txt_password_login
txt_password_login.next_field = txt_username_login


def btn_login_event():
    if len(txt_username_login.text) < 1:
        lbl_login_msg.text = lang_config[LANGUAGE]["invalid_login"]
        return
    if len(txt_password_login.text) < 1:
        lbl_login_msg.text = lang_config[LANGUAGE]["invalid_login"]
        return
    packet = {
        "type": "LOGIN",
        "client_id": client_id,
        "username": txt_username_login.text,
        "password": txt_password_login.text
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    print(timenow() + str(network))
    network.send(json.dumps(packet).encode("utf-8"))
    lbl_register_msg.text = ""


btn_login = Button(
    text=lang_config[LANGUAGE]["login"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=login_menu,
    x=-0.15,
    y=-0.15,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_login.on_click = btn_login_event

btn_back_login = Button(
    text=lang_config[LANGUAGE]["return"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=login_menu,
    x=0.15,
    y=-0.15,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"],
    onclick=Func(btn_back_event)
)
btn_back_login.on_click = btn_back_event

# Register Menu

register_menu_back = Entity(
    model="cube",
    color=themes[THEME]["ui_background"],
    scale_x=0.6,
    scale_y=0.6,
    position_z=1,
    parent=register_menu
)

lbl_username_register = Text(
    text=lang_config[LANGUAGE]["username"],
    x=-0.25,
    y=0.25,
    parent=register_menu
)

lbl_password_register = Text(
    text=lang_config[LANGUAGE]["password"],
    x=-0.25,
    y=0.15,
    parent=register_menu
)

lbl_email = Text(
    text=lang_config[LANGUAGE]["email"],
    x=-0.25,
    y=0.05,
    parent=register_menu
)

lbl_register_msg = Text(
    text="",
    x=-0.25,
    y=-0.05,
    parent=register_menu
)

txt_username_register = InputField(
    color=color.black,
    y=0.2,
    parent=register_menu
)

txt_password_register = InputField(
    color=color.black,
    y=0.1,
    hide_content=True,
    parent=register_menu
)

txt_email_register = InputField(
    color=color.black,
    parent=register_menu
)

txt_username_register.next_field = txt_password_register
txt_password_register.next_field = txt_email_register
txt_email_register.next_field = txt_username_register


def btn_register_event():
    if len(txt_username_register.text) < 1:
        lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_username"]
        return
    if len(txt_password_register.text) < 1:
        lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_password"]
        return
    if len(txt_email_register.text) < 1:
        lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_email"]
        return
    packet = {
        "type": "REGISTER",
        "client_id": client_id,
        "username": txt_username_register.text,
        "password": txt_password_register.text,
        "email": txt_email_register.text,
    }
    print(timenow() + "sending packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    lbl_register_msg.text = ""


btn_register = Button(
    text=lang_config[LANGUAGE]["register"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=register_menu,
    x=-0.15,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_register.on_click = btn_register_event

btn_back_register = Button(
    text=lang_config[LANGUAGE]["return"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=register_menu,
    x=0.15,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_back_register.on_click = btn_back_event

# Register Success Menu

lbl_register_success = Text(
    text=lang_config[LANGUAGE]["register_success"],
    origin=(0, 0),
    y=-0.05,
    parent=register_success_menu
)

btn_back_register_success = Button(
    text=lang_config[LANGUAGE]["return"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=register_success_menu,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_back_register_success.on_click = btn_back_event


# Main Menu

def btn_battle_main_event():
    packet = {
        "type": "ENTER_LOBBY",
        "client_id": client_id
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    lobby_menu.enabled = True
    lbl_lobby.text = ""
    main_menu.enabled = False


btn_battle_main = Button(
    text=lang_config[LANGUAGE]["battle"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=main_menu,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_battle_main.on_click = btn_battle_main_event

btn_quit_main = Button(
    text=lang_config[LANGUAGE]["quit"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=main_menu,
    x=-0.15,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_quit_main.on_click = btn_quit_event


def btn_logout_main_event():
    packet = {
        "type": "LOGOUT",
        "client_id": client_id
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    init_menu.enabled = True
    main_menu.enabled = False


btn_logout_main = Button(
    text=lang_config[LANGUAGE]["logout"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=main_menu,
    x=0.15,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_logout_main._on_click = btn_logout_main_event


# Lobby Menu:

def btn_return_lobby_event():
    packet = {
        "type": "LEAVE_LOBBY",
        "client_id": client_id
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    main_menu.enabled = True
    lobby_menu.enabled = False


btn_return_lobby = Button(
    text=lang_config[LANGUAGE]["return"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=lobby_menu,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_return_lobby._on_click = btn_return_lobby_event

lbl_lobby = Text(
    text=lang_config[LANGUAGE]["waiting_lobby"],
    y=0.25,
    parent=lobby_menu
)


# In-Game Menu:

def btn_leave_game_event():
    packet = {
        "type": "LEAVE_MAP",
        "client_id": client_id
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    in_game_menu.enabled = False
    main_menu.enabled = True
    ground.color = map_models["default"]["GROUND_COLOR"]
    ground.texture = map_models["default"]["GROUND_TEXTURE"]
    ground.texture_scale = map_models["default"]["GROUND_TEXTURE_SCALE"]


btn_leave_game = Button(
    text=lang_config[LANGUAGE]["leave_map"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=in_game_menu,
    x=-0.2,
    y=-0.2,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_leave_game._on_click = btn_leave_game_event


def btn_logout_game_event():
    packet = {
        "type": "LOGOUT",
        "client_id": client_id
    }
    print(timenow() + "packet to server: " + json.dumps(packet))
    network.send(json.dumps(packet).encode("utf-8"))
    in_game_menu.enabled = False
    init_menu.enabled = True
    ground.color = map_models["default"]["GROUND_COLOR"]
    ground.texture = map_models["default"]["GROUND_TEXTURE"]
    ground.texture_scale = map_models["default"]["GROUND_TEXTURE_SCALE"]


btn_logout_game = Button(
    text=lang_config[LANGUAGE]["logout"],
    color=themes[THEME]["ui_button"],
    highlight_color=themes[THEME]["ui_button"],
    parent=in_game_menu,
    x=-0.2,
    y=-0.3,
    scale_x=themes[THEME]["button_scale_x"],
    scale_y=themes[THEME]["button_scale_y"]
)
btn_logout_game._on_click = btn_logout_game_event


def timenow():
    return str(datetime.datetime.now()) + " "


# Main server connection loop:
while True:
    network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    network.settimeout(10)
    error_occurred = False
    try:
        network.connect((SERVER_HOST, SERVER_PORT))
        client_id = network.recv(PACKET_SIZE).decode("utf8")
        print(timenow() + "server connection established")
        print(timenow() + str(network))
    except ConnectionRefusedError:
        print(timenow() + "unable to connect to host server")
        error_occurred = True
    except socket.timeout:
        print(timenow() + "server connection timed out")
        error_occurred = True
    except socket.gaierror:
        print(timenow() + "unable to connect to host server")
        error_occurred = True
    finally:
        network.settimeout(None)
    if not error_occurred:
        break


def register_status(status):
    if status:
        txt_username_register.clear()
        txt_password_register.clear()
        txt_email_register.clear()
        register_success_menu.enabled = True
        register_menu.enabled = False
    else:
        lbl_register_msg.text = lang_config[LANGUAGE]["register_error"]


def login_status(status):
    if status:
        txt_username_login.clear()
        txt_password_login.clear()
        main_menu.enabled = True
        login_menu.enabled = False
    else:
        lbl_login_msg.text = lang_config[LANGUAGE]["invalid_login"]


def update_pos(entity_name):
    print("updating entity=" + entity_name)


def enter_map(map_name):
    load_map(map_name)
    in_game_menu.enabled = True
    lobby_menu.enabled = False


def load_map(map_name):
    print("loading map=" + map_name)
    ground.color = map_models[map_name]["GROUND_COLOR"]
    ground.texture = map_models[map_name]["GROUND_TEXTURE"]
    ground.texture_scale = map_models[map_name]["GROUND_TEXTURE_SCALE"]


def listen():
    while True:
        try:
            handle_packet()
        except Exception as e:
            print(e)
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
    # player_model.z += cos(radians(move_direction)) * move_speed
    # player_model.x += sin(radians(move_direction)) * move_speed
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
    color=map_models["default"]["GROUND_COLOR"],
    texture=map_models["default"]["GROUND_TEXTURE"],
    texture_scale=map_models["default"]["GROUND_TEXTURE_SCALE"],
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

# camera.z = -5
player_model.enabled = False
player_camera.enabled = False

if __name__ == "__main__":
    main()
