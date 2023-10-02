from ursina import *

# Map model used by the client

class Map:
    def __init__(self):
        super().__init__(
            parent=camera.ui
        )

        MAP_WIDTH = 1000
        clients = {}
        floor = Entity(
            model="plane",
            scale=(MAP_WIDTH, 1, MAP_WIDTH),
            position=(0, 0, 0),
            color=color.light_gray,
            texture="white_cube",
            texture_scale=(100, 100),
            collider="box"
        )

        flavor_text = {
            "english": "map1 flavor text"
        }
