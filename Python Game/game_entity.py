from ursina import Entity


class GameEntity(Entity):
    def __init__(self, entity_name, pos_x, pos_y, max_health, health):
        super().__init__()
        self.entity_name = entity_name
        self.position_x = pos_x
        self.position_y = pos_y
        self.max_health = max_health
        self.health = health
