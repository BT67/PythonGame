# Map entity used by the client
from ursina import Entity


class ClientMap(Entity):
    def __init__(self, map_name):
        super().__init__()
        self.map_name = map_name
        self.clients = []
        self.size = 1000
        self.ground_texture = None
        self.ground_color = None
        self.is_full = False
