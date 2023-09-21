from ursina import *

app = Ursina()


class Player(Entity):
    def __init__(self, x, y, speed):
        super().__init__()
        self.model = "cube"
        self.color = color.light_gray
        self.texture = "white_cube"
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        if held_keys['up arrow']:
            self.y += self.speed
        if held_keys['left arrow']:
            self.x -= self.speed
        if held_keys['down arrow']:
            self.y -= self.speed
        if held_keys['right arrow']:
            self.x += self.speed

def change_color():
    button.color = color.red

def update():
    # cube1.x = cube1.x + time.dt
    if held_keys['w']:
        camera.y += 0.1
    if held_keys['a']:
        camera.x -= 0.1
    if held_keys['s']:
        camera.y -= 0.1
    if held_keys['d']:
        camera.x += 0.1



# Z-axis + moves further away, z-axis - moves towards the camera

# Creating entities:
cube1 = Entity(
    model="cube",
    rotation=(45, 15, 0),
    scale=(1, 1, 1),
    position=(-6, 0, 0),
    color=color.gray,
    texture="brick",
    collider="box"
)

cubes = [cube1]

dx = 0.1

cube2 = Entity(
    model="cube",
    rotation=(45, 15, 0),
    scale=(1, 5, 5),
    position=(0, 0, 0),
    color=color.light_gray,
    texture="sky_sunset",
    collider="box"
)

button = Button(
    color=color.black,
    text="BUTTON",
    scale=(0.5, 0.25,0),
    model="cube"
)

button.on_click = change_color
button.tooltip = Tooltip("test button")

player = Player(5, 5, 0.1)

text1 = Text(
    text="text",
    color=color.green,
    scale=(2, 2, 2)
)

app.run()
