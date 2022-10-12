import random


class Gaming:
    def __init__(self):
        self.x_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.y_tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
        self.field_dict = {}
        #self.schedule = False
        self.boats_coordinate = []

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

    def gaming(self, x, y):
        if self.field_dict[int(x)][str(y)] == 'empty':
            self.field_dict[int(x)][str(y)] = 'burned/empty'
            result = self.field_dict[int(x)][str(y)]
            #self.schedule = True
        elif self.field_dict[int(x)][str(y)] == 'boat':
            self.field_dict[int(x)][str(y)] = 'burned/boat'
            result = self.field_dict[int(x)][str(y)]
            #self.schedule = True
        elif self.field_dict[int(x)][str(y)] == 'burned/boat' or 'burned/empty':
            #self.schedule = False
            result = 'You already fired'
        return self.field_dict, result

    # def input_coordinate(self):
    #     x = 0
    #     while x not in self.x_tuple:
    #         try:
    #             x = int(input("Please enter your coordinate (1 - 10) :"))
    #         except:
    #             print('It must be digit')
    #     y = 'z'
    #     while not str(y) in self.y_tuple:
    #         y = input("Please enter your coordinate (a - j) :")
    #     return x, y
    #
    # def play(self):
    #     stop = None
    #     while not stop:
    #         stop = input('Exit?')
    #         x, y = self.input_coordinate()
    #         self.gaming(x, y)

    def get_field_dict(self):
        return self.field_dict

    def find_full_boat(self, x, y):
        for boat_coordinate in self.boats_coordinate:
            for x_boat, y_list in boat_coordinate.items():
                for y_boat in y_list:
                    if x == x_boat and y == y_boat:
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

#
# a = Gaming()
# a.set_dict()
# a.random_boats()
