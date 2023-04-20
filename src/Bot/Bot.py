from random import randrange
import time

from src.constants import LIST_OF_SHIPS, DEFAULT_SIZE, MAX_NUMBER_OF_RETRIES, Status


class Bot:
    remaining_ships = 10
    ships = []

    def __init__(self, sys):
        self.sys = sys

    @staticmethod
    def generate_coordinates(range_):
        """this func generates a pair of coordinates in chosen range
            returns them as a list of 2 elements"""
        return [randrange(0, range_), randrange(0, range_)]

    def generate_ships(self):
        """this func randomly generates ship's coordinates
            returns True if generation ended successfully else False"""
        self.ships = []
        for ship_size in LIST_OF_SHIPS:

            generation_successful = False
            retry_ = 0

            while not generation_successful:

                if retry_ > MAX_NUMBER_OF_RETRIES:
                    return False

                xy = self.generate_coordinates(DEFAULT_SIZE)
                coords = [[a, xy[1]] for a in range(xy[0], xy[0] + ship_size)]
                coords1 = [[xy[0], b] for b in range(xy[1], xy[1] + ship_size)]

                if self.sys.get_field().does_ship_fit(coords, False):
                    self.sys.get_game().create_ship(coords, self.sys.get_field().bot_field)
                    generation_successful = True

                elif self.sys.get_field().does_ship_fit(coords1, False):
                    self.sys.get_game().create_ship(coords1, self.sys.get_field().bot_field)
                    generation_successful = True

                else:
                    retry_ += 1

        return True

    def make_shot(self):
        retry = 0

        x, y = self.generate_coordinates(DEFAULT_SIZE)

        while (self.sys.get_field().player_field[x][y].status == Status.dead.name
               or self.sys.get_field().player_field[x][y].status == Status.miss.name) and retry < MAX_NUMBER_OF_RETRIES:
            x = randrange(0, DEFAULT_SIZE)
            y = randrange(0, DEFAULT_SIZE)
            retry += 1

        time.sleep(0.5)

        self.sys.get_game().make_shot(x, y)