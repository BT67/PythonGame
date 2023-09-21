from ursina import Entity, Vec3


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.focused = False
        self.target = Vec3(0, 0, 0)
        self.on_click = self.set_focused

    def set_focused(self):
        self.focused = True

    def set_unfocused(self):
        self.focused = False

