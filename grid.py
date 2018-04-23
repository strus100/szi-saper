from field import Field
import random

class Grid:

    def __init__(self, width, height, field_width, field_height):

        self.grid = []
        self.width = width
        self.height = height
        self.path = []

        self.drawing_height = height*field_height
        self.drawing_width = width*field_width

        for y in range(0, height):
            horizontal = []
            for x in range(0, width):
                is_wall_field = random.randrange(12) != 1
                field = Field(x, y, {'is_bomb': False}, field_width, field_height, is_wall_field, self.is_bomb_field(is_wall_field, x, y))
                horizontal.insert(len(horizontal), field)
            self.grid.insert(len(self.grid), horizontal)

    def is_bomb_field(self, is_walkable, x, y):
        if is_walkable:
            return random.randrange(30) == 1 or y == 5 and x == 5
        else:
            return False

    def get_neighbours(self, field):
        neighbours = []

        for x in range(-100, 101, 100):
            for y in range(-100, 101, 100):
                if x == 0 and y == 0:
                    continue
                
                check_x = field.x + x
                check_y = field.y + y

                x_index = int(check_x*0.01)
                y_index = int(check_y*0.01)

                if (x_index >= 0 and x_index < self.width and y_index >= 0 and y_index < self.height):
                    
                    neighbours.insert(len(neighbours), self.grid[y_index][x_index])

        return neighbours

    def set_path(self, path):
        self.path = path

    def first_and_last(self):
        return [self.grid[0][0], self.grid[self.width-1][self.height-1]]