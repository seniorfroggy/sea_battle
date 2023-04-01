from constants import *
from random import randrange

class Bot:
    remaining_ships = 10
    ships = []

    def __init__(self, sys):
        self.sys = sys

    def generate_ships(self):
        self.ships = []
        for ship_size in LIST_OF_SHIPS:

            flag = False
            retry_ = 0

            while not flag:

                if retry_ > 50:
                    return False

                xy = [randrange(0, DEFAULT_SIZE), randrange(0, DEFAULT_SIZE)]
                coords = [[a, xy[1]] for a in range(xy[0], xy[0] + ship_size)]
                coords1 = [[xy[0], b] for b in range(xy[1], xy[1] + ship_size)]

                if self.sys.get_field().does_ship_fit(coords, False):
                    self.sys.get_game().create_ship(coords, self.sys.get_field().bot_field)
                    flag = True

                elif self.sys.get_field().does_ship_fit(coords1, False):
                    self.sys.get_game().create_ship(coords1, self.sys.get_field().bot_field)
                    flag = True

                else:
                    retry_ += 1

        return True

    def make_shot(self):
        retry = 0

        x = randrange(0, DEFAULT_SIZE)
        y = randrange(0, DEFAULT_SIZE)

        while (self.sys.get_field().player_field[x][y].status == "dead"
               or self.sys.get_field().player_field[x][y].status == "miss") and retry < 50:
            x = randrange(0, DEFAULT_SIZE)
            y = randrange(0, DEFAULT_SIZE)
            retry += 1
            self.sys.get_tk().update()

        self.sys.get_game().make_shot(x, y)