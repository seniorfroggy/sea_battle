from src.constants import MARGIN, LIST_OF_SHIPS_REM


class Player:
    coords_container = []
    remaining_ships = 10
    ships = []

    def __init__(self, sys):
        self.sys = sys

    def add_ship_position(self, xc, yc):
        if not self.sys.get_field().are_coords_valid(xc, yc):
            self.sys.get_interface().show_warning()
            return

        self.sys.get_interface().hide_warning()

        self.coords_container.append([xc, yc])

        self.sys.get_interface().draw_part_of_the_ship(xc, yc, [[MARGIN, MARGIN], [MARGIN, MARGIN]], "blue", "temp")

        if len(self.coords_container) == LIST_OF_SHIPS_REM[0]:

            if self.sys.get_game().is_ship_valid(self.coords_container):
                self.sys.get_game().create_ship(self.coords_container, self.sys.get_field().player_field)
                LIST_OF_SHIPS_REM.pop(0)
                self.coords_container = []

                if not LIST_OF_SHIPS_REM:
                    self.sys.get_game().start()
                    return

                self.sys.get_interface().hide_warning()

                s = "Place {deck}-deck ship".format(deck=LIST_OF_SHIPS_REM[0])
                self.sys.get_interface().main_label.configure(text=s)

            else:
                self.sys.get_interface().delete_by_tag("temp")

                self.sys.get_interface().show_warning()

                self.coords_container = []