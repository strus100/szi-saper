class AStar:
    def find_path(self, start_field, target_field, grid):
        open_set = []
        closed_set = []
        open_set.insert(0, start_field)

        while len(open_set) > 0:
            current_field = open_set[0]
            for open_field in open_set:
                if open_field.f_cost() < current_field.f_cost() or open_field.f_cost == current_field.f_cost and open_field.h_cost < current_field.h_cost:
                    current_field = open_field

            open_set.remove(current_field)
            closed_set.insert(len(closed_set), current_field)

            if current_field == target_field:
                print("ZNALAZLEM")
                return self.retrace_path(start_field, target_field)

            for neighbour in grid.get_neighbours(current_field):
                if not neighbour.walkable or neighbour in closed_set:
                    continue

                new_movement_cost_to_neighbour = current_field.g_cost + self.get_distance(current_field, neighbour)
                if new_movement_cost_to_neighbour < neighbour.g_cost or not neighbour in open_set:
                    neighbour.g_cost = new_movement_cost_to_neighbour
                    neighbour.h_cost = self.get_distance(neighbour, target_field)
                    neighbour.set_parent(current_field)

                    if not neighbour in open_set:
                        open_set.insert(len(open_set), neighbour)
    def retrace_path(self, start_field, end_node):
        path = []
        current_field = end_node

        while (current_field != start_field):
            path.insert(len(path), current_field)
            current_field = current_field.parent

        path.insert(len(path), start_field)
        path = path[::-1]
        return path

    def get_distance(self, field_a, field_b):
        if field_b.is_water:
            special_x = 40
        elif field_b.is_mud:
            special_x = 20
        else:
            special_x = 10

        dist_x = abs(field_a.map_x - field_b.map_x)
        dist_y = abs(field_a.map_y - field_b.map_y)

        if dist_x > dist_y:
            return (14*dist_y + 10*(dist_x-dist_y))*special_x
        return (14*dist_y + 10*(dist_y-dist_x))*special_x
