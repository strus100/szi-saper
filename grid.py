from field import Field
import random




class Grid:

    def __init__(self, how_many_fields, field_size, params_data):
        self.grid = []
        self.how_many_fields = how_many_fields
        self.path = []

        self.drawing_size = how_many_fields*field_size

        for y in range(0, how_many_fields):
            horizontal = []
            for x in range(0, how_many_fields):
                is_wall_field = self.is_wall_field(how_many_fields, x, y)
                is_mud = self.is_special_field(not is_wall_field)
                is_water = self.is_special_field(not is_wall_field) if not is_mud else False
                is_bomb = self.is_bomb_field(not is_wall_field, not is_water)
                field_params = self.generate_params(params_data, is_bomb)
                field = Field(x, y, field_params, field_size, not is_wall_field, is_bomb, is_mud, is_water)
                horizontal.insert(len(horizontal), field)
            self.grid.insert(len(self.grid), horizontal)

    def is_wall_field(self, how_many_fields, x, y):
        if (x == (how_many_fields-1) and (y == (how_many_fields-1))):
            is_wall_field = False
        else:
            is_wall_field = random.randrange(8) == 1
        return is_wall_field

    def is_special_field(self, is_walkable):
        if is_walkable:
            return random.randrange(5) == 1
        else:
            return False

    def is_bomb_field(self, is_walkable, is_not_water):
        if is_walkable and is_not_water:
            return random.randrange(20) == 1
        else:
            return False

    def get_neighbours(self, field):
        neighbours = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                check_x = field.x + x
                check_y = field.y + y

                if (check_x >= 0 and check_x < self.how_many_fields and check_y >= 0 and check_y < self.how_many_fields):
                    neighbours.insert(len(neighbours), self.grid[check_y][check_x])

        return neighbours

    def set_path(self, path):
        self.path = path

    def first_and_last(self):
        last = self.how_many_fields -1
        return [self.grid[0][0], self.grid[last][last]]

    def generate_params(self, params_data, is_bomb):
        is_bomb = int(is_bomb)
        correct_params = list(filter(lambda x: x[-1] == f"{is_bomb}", params_data))
        correct_params = list(map(self.list_to_dict, correct_params))
        correct_params_amount = len(correct_params)
        n = random.randrange(correct_params_amount)
        return correct_params[n]

    def list_to_dict(self, params):
        [q,w,e,r,t] = params
        return {"is_beeping": q, "metal_detector_beeping": w, "is_dugged_up": e, "war_here": r}
