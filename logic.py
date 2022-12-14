import random


class Gaming:
    def __init__(self):
        self.x_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.y_tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
        self.field_dict = {}
        self.boats_coordinate = []
        self.list_coordinate_burn = []

    def set_dict(self):
        for digit in self.x_tuple:
            self.field_dict[digit] = {}
            for letter in self.y_tuple:
                self.field_dict[digit][letter] = 'empty'

    def random_boats(self):
        boats_set = {1: 4, 2: 3, 3: 2, 4: 1}
        for boat_deck in boats_set:
            boats_quantity = 0
            while boats_quantity < boats_set[boat_deck]:
                boat_coordinate = self.create_random_boat_coordinate(boat_deck)

                near_dict_final = self.create_near_dict(boat_coordinate)
                near_empty = self.check_boat_near(near_dict_final)
                if near_empty:
                    self.boats_coordinate.append(boat_coordinate)
                    for x, y_set in boat_coordinate.items():
                        for y in y_set:
                            self.field_dict[x][y] = 'boat'
                    boats_quantity += 1

    def random_x_y(self):
        x = int(random.choice(self.x_tuple))
        y = str(random.choice(self.y_tuple))
        return x, y

    def check_boat_near(self, near_dict_final, near_empty=True):
        for x_near, y_list_near in near_dict_final.items():
            for y_near in y_list_near:
                if self.field_dict[x_near][y_near] == 'boat':
                    near_empty = False
                    break
        return near_empty

    def create_near_dict(self, boat_coordinate):
        near_dict_final = {}
        for x, y_set in boat_coordinate.items():
            for y in y_set:
                near_dict = self.neighboring_coordinate(x, y)
                for key, value in near_dict.items():
                    if key in near_dict_final.keys():
                        near_dict_final[key].update(value)
                    else:
                        near_dict_final[key] = value
        return near_dict_final

    def create_random_boat_coordinate(self, quantity_deck):
        boat_ready = False

        while not boat_ready:
            axis = random.choice(('x', 'y'))
            x, y = self.random_x_y()
            boat_coordinate = {}
            if axis == 'x':
                if self.x_tuple.index(x) + quantity_deck <= 10:
                    for i in range(quantity_deck):
                        boat_coordinate.update({x + i: y})
                    boat_ready = True
                    return boat_coordinate
            else:
                if self.y_tuple.index(y) + quantity_deck <= 10:
                    boat_coordinate = {x: set()}
                    pos = self.y_tuple.index(y)
                    for i in range(quantity_deck):
                        boat_coordinate[x].add(self.y_tuple[pos + i])
                    boat_ready = True
                    return boat_coordinate

    def neighboring_coordinate(self, x, y):
        near_dict = {}
        if x == 1:
            x_list_near = [x, x + 1]
        elif x == 10:
            x_list_near = [x, x - 1]
        else:
            x_list_near = [x - 1, x, x + 1]
        if y == self.y_tuple[0]:
            y_list_near = {y, self.y_tuple[1]}
        elif y == self.y_tuple[9]:
            y_list_near = {self.y_tuple[8], y}
        else:
            pos = self.y_tuple.index(y)
            y_list_near = {self.y_tuple[pos - 1], y, self.y_tuple[pos + 1]}
        for x in x_list_near:
            near_dict.update({x: y_list_near})
        return near_dict

    def shoot(self, x, y):
        if self.field_dict[int(x)][str(y)] == 'empty' or self.field_dict[int(x)][str(y)] == 'impossible':
            self.field_dict[int(x)][str(y)] = 'burned/empty'
            result = self.field_dict[int(x)][str(y)]
        elif self.field_dict[int(x)][str(y)] == 'boat':
            self.field_dict[int(x)][str(y)] = 'burned/boat'
            result = self.field_dict[int(x)][str(y)]
        elif self.field_dict[int(x)][str(y)] == 'burned/boat' or 'burned/empty':
            result = 'You already fired'
        return self.field_dict, result

    def checker_point(self, x, y):
        return self.field_dict[int(x)][str(y)]

    def get_field_dict(self):
        return self.field_dict

    def get_list_coordinate_burn(self):
        return self.list_coordinate_burn

    def find_full_boat_trigger(self, x, y):
        boat_coordinate = self.find_full_boat(x, y)
        full_not_full = self.check_boat_burned(boat_coordinate)
        if full_not_full:
            return boat_coordinate

    def check_boat_burned(self, boat_coordinate, full_not_full=True):
        for x_boat, y_list in boat_coordinate.items():
            for y_boat in y_list:
                if self.field_dict[x_boat][y_boat] == 'boat':
                    full_not_full = False
                    return full_not_full
        return full_not_full

    def find_full_boat(self, x, y):
        for boat_coordinate in self.boats_coordinate:
            for x_boat, y_list in boat_coordinate.items():
                for y_boat in y_list:
                    if x == x_boat and y == y_boat:
                        return boat_coordinate

    def create_list_coordinates_burn(self, x, y):
        pos = self.y_tuple.index(y)
        if x > 1:
            self.list_coordinate_burn.append({x - 1: y})
        if x < 10:
            self.list_coordinate_burn.append({x + 1: y})
        if 0 < pos < 9:
            self.list_coordinate_burn.append({x: self.y_tuple[pos - 1]})
            self.list_coordinate_burn.append({x: self.y_tuple[pos + 1]})
        elif pos == 0:
            self.list_coordinate_burn.append({x: self.y_tuple[pos + 1]})
        elif pos == 9:
            self.list_coordinate_burn.append({x: self.y_tuple[pos - 1]})
        return self.list_coordinate_burn

    def clear_list_coordinates_burn(self):
        self.list_coordinate_burn = []
        return None

    def replace_list_coordinates_burn(self, boat_coordinate):
        self.clear_list_coordinates_burn()
        for x_boat, y_list_near in boat_coordinate.items():
            for y_boat in y_list_near:
                if self.field_dict[x_boat][y_boat] == 'boat':
                    self.list_coordinate_burn.append({x_boat: y_boat})
        return self.list_coordinate_burn

    def impossible_points_around(self, boat_coordinate):
        near_dict_final = self.create_near_dict(boat_coordinate)
        for x_near, y_list_near in near_dict_final.items():
            for y_near in y_list_near:
                if self.field_dict[x_near][y_near] == 'empty':
                    self.field_dict[x_near][y_near] = 'impossible'

    def check_all_burned(self):
        for boat_coordinate in self.boats_coordinate:
            for x, y_list in boat_coordinate.items():
                for y in y_list:
                    if self.field_dict[x][y] == 'boat':
                        return False
        return True

    def replace_if_need_finished_burn(self, x, y):
        boat_coordinate_whole = self.find_full_boat(x, y)
        quantity_burned = 0
        for x_boat, y_list in boat_coordinate_whole.items():
            for y_boat in y_list:
                if self.field_dict[x_boat][y_boat] == 'burned/boat':
                    quantity_burned += 1
        if quantity_burned > 1:
            self.replace_list_coordinates_burn(boat_coordinate_whole)

    def random_from_list_to_burn(self):
        list_coordinates = random.choice(list(self.list_coordinate_burn))
        self.list_coordinate_burn.remove(list_coordinates)
        x = list(list_coordinates.keys())[0]
        y = list_coordinates[list(list_coordinates.keys())[0]]
        result_check = self.checker_point(x, y)
        if result_check == 'You already fired' or result_check == 'burned/boat' or \
                result_check == 'burned/empty' or result_check == 'impossible':
            return self.random_from_list_to_burn()
        return x, y

    def random_from_all(self):
        x, y = self.random_x_y()
        result_check = self.checker_point(x, y)
        if result_check == 'You already fired' or result_check == 'burned/boat' or \
                result_check == 'burned/empty' or result_check == 'impossible':
            return self.random_from_all()
        else:
            return x, y