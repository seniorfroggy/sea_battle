from src.constants import DEFAULT_ENEMY_SHIPS, GameStatus, Status, DEFAULT_SIZE, MAX_NUMBER_OF_RETRIES, BOT_FIELD_SHIFT
from src.Game.Ship.Ship import Ship


class Game:
    player_turn = True

    def __init__(self, status, ships, sys):
        self.status = status
        self.ships_to_place = ships
        self.sys = sys

    def is_ship_valid(self, coords):
        """this func checks if a ship can be constructed from the given coordinates
            returns true if can else false"""
        coords.sort()
        setx = set()
        sety = set()
        is_valid = True

        for pair in zip(coords, coords[1:]):
            setx.add(pair[0][0])
            setx.add(pair[1][0])
            sety.add(pair[0][1])
            sety.add(pair[1][1])
            if abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1]) != 1:

                is_valid = False
                break

        if not is_valid:
            return False

        for xy in coords:
            setx.add(xy[0])
            sety.add(xy[1])

        is_valid = len(setx) == 1 or len(sety) == 1

        if not is_valid:
            return False
        return self.sys.get_field().does_ship_fit(coords, True)

    def create_ship(self, coords, field):
        """this func takes coordinates and creates a ship there"""
        ship = Ship(coords, Status.alive.name)
        for i in range(len(coords)):
            xy = coords[i]
            field[xy[0]][xy[1]].status = Status.alive.name
            field[xy[0]][xy[1]].ship = ship

        if field == self.sys.get_field().player_field:
            self.sys.get_interface().draw_ship(coords, True)
            self.sys.get_player().ships.append(ship)
        else:
            self.sys.get_bot().ships.append(ship)

    def start(self):
        """this func sets bot ships if their generation ended unsuccessfully, outputs rules and starts in-game music"""
        self.sys.get_interface().hide_warning()
        self.sys.get_interface().delete_by_tag("temp")
        attempt = 0
        while not self.sys.get_bot().generate_ships():
            attempt += 1
            if attempt > MAX_NUMBER_OF_RETRIES * MAX_NUMBER_OF_RETRIES:
                self.sys.get_bot().ships = []
                for x_, y_ in [(i, j) for i in range(DEFAULT_SIZE) for j in range(DEFAULT_SIZE)]:
                    self.sys.get_field().bot_field[x_][y_].status = Status.blank.name
                    self.sys.get_field().bot_field[x_][y_].ship = None

                for coord in DEFAULT_ENEMY_SHIPS:
                    self.sys.get_bot().ships.append(Ship(coord, Status.alive.name))
                for item in self.sys.get_bot().ships:
                    for xy in item.coords:
                        self.sys.get_field().bot_field[xy[0]][xy[1]].status = Status.alive.name
                break
        self.status = GameStatus.play.name
        self.sys.get_interface().main_label.configure(foreground="black")
        self.sys.get_interface().output_rules()
        self.sys.get_interface().play_sound("src/music/pirates2.mp3")

    def end(self):
        """this func outputs a text in the end of the game depending on its result"""
        res = ("LOST!" if self.sys.get_bot().remaining_ships != 0 else "WON!")
        color = ("red" if res == "LOST!" else "green")
        self.sys.get_interface().output_result(res, color)
        self.status = GameStatus.finished.name

    def make_shot(self, xc, yc):
        """this func takes a pair of coordinates and shows warning/calls change_cell_status() depending on the arguments"""
        if (BOT_FIELD_SHIFT > xc >= DEFAULT_SIZE) or not (0 <= yc < DEFAULT_SIZE) or\
                (self.sys.get_game().player_turn and (xc < DEFAULT_SIZE or xc > BOT_FIELD_SHIFT + 9)):

            self.sys.get_interface().show_warning()

            return

        self.sys.get_interface().hide_warning()

        self.sys.get_field().change_cell_status(xc, yc)

        self.check_game_finished()

    def check_game_finished(self):
        """this func checks if one of the players has lost all the ships and calls end() if one was found"""
        if self.sys.get_bot().remaining_ships * self.sys.get_player().remaining_ships == 0:
            self.end()

