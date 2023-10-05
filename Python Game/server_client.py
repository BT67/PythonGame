

class ServerClient:
    def __init__(self, client_id, connection):
        self.connection = connection
        self.client_id = client_id
        self.username = None
        self.pos_x = None
        self.pos_y = None
        self.pos_z = None
        self.target_x = None
        self.target_y = None
        self.target_z = None
        self.in_battle = False
        self.current_map = None
        self.max_health = None
        self.health = None
        self.attack_damage = None
        self.move_speed = None
        self.acceleration = None
        self.power = None
        self.drag = None
        self.rotation_x = None
        self.rotation_y = None
        self.rotation_z = None
        self.max_speed = None
        self.reverse = False
        self.turning_left = False
        self.turning_right = False
        self.moving_forward = False
        self.moving_backward = False


