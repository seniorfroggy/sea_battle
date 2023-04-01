from constants import *
from class_Game.class_Ship.Ship import *
from tkinter import messagebox

class Game:
    player_turn = True

    def __init__(self, status, ships, sys):
        self.status = status
        self.ships_to_place = ships
        self.sys = sys

    def is_ship_valid(self, coords):
        coords.sort()
        setx = set()
        sety = set()
        flag = True

        for pair in zip(coords, coords[1:]):
            setx.add(pair[0][0])
            setx.add(pair[1][0])
            sety.add(pair[0][1])
            sety.add(pair[1][1])
            if abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1]) != 1:

                flag = False
                break

        if not flag:
            return False

        for xy in coords:
            setx.add(xy[0])
            sety.add(xy[1])

        flag = len(setx) == 1 or len(sety) == 1

        if not flag:
            return False
        return self.sys.get_field().does_ship_fit(coords, True)

    def create_ship(self, coords, f):
        ship = Ship(coords, "alive")
        for i in range(len(coords)):
            xy = coords[i]
            f[xy[0]][xy[1]].status = "alive"
            f[xy[0]][xy[1]].ship = ship

        if f == self.sys.get_field().player_field:
            self.sys.get_interface().draw_ship(coords, "ally")
            self.sys.get_player().ships.append(ship)
        else:
            self.sys.get_bot().ships.append(ship)

    def start(self):
        self.sys.get_interface().hide_t2_label()
        self.sys.get_interface().delete_by_tag("temp")
        attempt = 0
        while not self.sys.get_bot().generate_ships():
            attempt += 1
            if attempt > 1000:
                self.sys.get_bot().ships = []
                for x_ in range(10):
                    for y_ in range(10):
                        self.sys.get_field().bot_field[x_][y_].status = "blank"
                        self.sys.get_field().bot_field[x_][y_].ship = None

                for coord in DEFAULT_ENEMY_SHIPS:
                    self.sys.get_bot().ships.append(Ship(coord, "alive"))
                for item in self.sys.get_bot().ships:
                    for xy in item.coords:
                        self.sys.get_field().bot_field[xy[0]][xy[1]].status = "alive"
                break
        self.status = "play"
        self.sys.get_interface().t1.configure(foreground="black")
        self.sys.get_interface().output_rules()

    def end(self):
        res = ("LOST!" if self.sys.get_bot().remaining_ships != 0 else "WON!")
        color = ("red" if res == "LOST!" else "green")
        self.sys.get_interface().draw_result(res, color)
        self.status = "finished"

    def make_shot(self, xc, yc):
        if (xc >= 10 >= yc) or (yc >= 10 >= xc) or (self.sys.get_game().player_turn and (xc < 10 or yc < 10)):

            self.sys.get_interface().show_t2_label()

            return

        self.sys.get_interface().hide_t2_label()

        self.sys.get_field().change_cell_status(xc, yc)

        self.check_game_finished()

    def check_game_finished(self):
        if self.sys.get_bot().remaining_ships * self.sys.get_player().remaining_ships == 0:
            self.end()

    def exiting(self):
        if messagebox.askokcancel("Exiting", "Wanna leave?"):
            self.sys.get_game().status = "finished_exit"
            self.sys.get_tk().destroy()