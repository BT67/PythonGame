

class ServerClient:
    def __init__(self, client_id, connection):
        self.connection = connection
        self.client_id = client_id
        self.username = None
        self.pos_x = None
        self.pos_y = None
        self.target_x = None
        self.target_y = None
        self.in_battle = False
        self.current_map = None
        self.max_health = None
        self.health = None
        self.attack_damage = None


