from ursina import *

# Map models used by the client

map_models = {}

MAP_WIDTH = 1000

map_models["default"] = {
    "MAP_WIDTH": MAP_WIDTH,
    "GROUND_COLOR": color.light_gray,
    "GROUND_TEXTURE": "white_cube",
    "GROUND_TEXTURE_SCALE": (100, 100),
    "flavor_text": {
        "english": "default map flavor text"
    }
}

map_models["map1"] = {
    "MAP_WIDTH": MAP_WIDTH,
    "GROUND_COLOR": color.green,
    "GROUND_TEXTURE": "white_cube",
    "GROUND_TEXTURE_SCALE": (100, 100),
    "flavor_text": {
        "english": "map1 flavor text"
    }
}



