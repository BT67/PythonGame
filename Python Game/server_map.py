
class ServerMap:
    def __init__(self, map_name):
        self.map_name = map_name
        self.clients = []
        self.size = 1000
        self.ground_texture = None
        self.ground_color = None
        self.is_full = False
