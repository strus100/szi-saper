class Field:
    def __init__(self, x, y, params, size, walkable = True, has_bomb = False):
        self.x = x
        self.y = y
        self.map_x = x * size
        self.map_y = y * size
        self.params = params
        self.walkable = walkable
        self.has_bomb = has_bomb

        self.color = (0,0,0) if not walkable else (0,255,0)

        self.g_cost = 0
        self.h_cost = 0

    def get_position(self):
        return (self.x, self.y)

    def f_cost(self):
        return self.g_cost + self.h_cost

    def set_parent(self, parent):
        self.parent = parent
