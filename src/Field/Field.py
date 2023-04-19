from src.constants import DEFAULT_SIZE, Status, BOT_FIELD_SHIFT
from src.Field.Cell.Cell import Cell
import copy


class Field:
    x_cells, y_cells = DEFAULT_SIZE, DEFAULT_SIZE
    player_field = [[Cell(Status.blank.name, [i, j], None) for j in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
    bot_field = copy.deepcopy(player_field)

    def __init__(self, sys, field_size):
        self.sys = sys
        self.x_cells = self.y_cells = field_size

    @staticmethod
    def are_coords_valid(xc, yc):
        return 0 <= xc < DEFAULT_SIZE and 0 <= yc < DEFAULT_SIZE

    def is_ship_destroyed(self, xc, yc):
        cnt = 0
        field = (self.bot_field if self.sys.get_game().player_turn else self.player_field)
        while xc + 1 < DEFAULT_SIZE and (field[xc + 1][yc].status == Status.alive.name or
                                         field[xc + 1][yc].status == Status.dead.name):
            cnt += (1 if field[xc + 1][yc].status == Status.alive.name else 0)
            xc += 1
        while yc + 1 < DEFAULT_SIZE and (field[xc][yc + 1].status == Status.alive.name or field[xc][yc + 1].status == Status.dead.name):
            cnt += (1 if field[xc][yc + 1].status == Status.alive.name else 0)
            yc += 1
        while xc - 1 >= 0 and (field[xc - 1][yc].status == Status.alive.name or field[xc - 1][yc].status == Status.dead.name):
            cnt += (1 if field[xc - 1][yc].status == Status.alive.name else 0)
            xc -= 1
        while yc - 1 >= 0 and (field[xc][yc - 1].status == Status.alive.name or field[xc][yc - 1].status == Status.dead.name):
            cnt += (1 if field[xc][yc - 1].status == Status.alive.name else 0)
            yc -= 1
        return cnt == 0

    def change_cell_status(self, xc, yc):
        on_players_field = True
        if xc > 10:
            on_players_field = False
            xc -= BOT_FIELD_SHIFT

        if on_players_field:
            self.change_players_cell_status(xc, yc)
        else:
            self.change_bot_cell_status(xc, yc)

    def change_players_cell_status(self, xc, yc):
        if self.sys.get_field().player_field[xc][yc].status == Status.blank.name:
            self.sys.get_field().player_field[xc][yc].status = Status.miss.name

            self.sys.get_interface().mark_as_miss(xc, yc)

            self.sys.get_game().player_turn = not self.sys.get_game().player_turn

        if self.sys.get_field().player_field[xc][yc].status == Status.alive.name:
            self.sys.get_field().player_field[xc][yc].status = Status.dead.name
            self.sys.get_field().player_field[xc][yc].ship.hp -= 1

            self.sys.get_interface().draw_hit(xc, yc)

            self.sys.get_interface().play_temp_sound("src/music/bot_hit_sound.mp3", 0.5)

            if self.is_ship_destroyed(xc, yc):
                self.sys.get_player().remaining_ships -= 1
                self.player_field[xc][yc].ship.status = Status.dead.name

                self.sys.get_interface().change_number_of_ships()

    def change_bot_cell_status(self, xc, yc):
        if self.sys.get_field().bot_field[xc][yc].status == Status.blank.name:
            self.sys.get_field().bot_field[xc][yc].status = Status.miss.name

            self.sys.get_interface().mark_as_miss(xc + BOT_FIELD_SHIFT, yc)

            self.sys.get_interface().play_temp_sound("src/music/player_miss_sound.mp3", 0.5)

            self.sys.get_game().player_turn = not self.sys.get_game().player_turn

        if self.sys.get_field().bot_field[xc][yc].status == Status.alive.name:
            self.sys.get_field().bot_field[xc][yc].status = Status.dead.name

            self.sys.get_interface().play_temp_sound("src/music/player_hit_sound.mp3", 0.5)

            self.sys.get_interface().mark_as_hit(xc + BOT_FIELD_SHIFT, yc)

            if self.is_ship_destroyed(xc, yc):
                self.sys.get_bot().remaining_ships -= 1

    def does_ship_fit(self, coords, flag):
        if flag:
            field_ = self.sys.get_field().player_field
        else:
            field_ = self.sys.get_field().bot_field
        does_fit = True
        for xy in coords:
            x = xy[0]
            y = xy[1]
            does_fit &= self.are_coords_valid(x, y)
            if not does_fit:
                return False
            if x != 0:

                does_fit &= (field_[x - 1][y].status == Status.blank.name)

                if y != 0:
                    does_fit &= field_[x - 1][y - 1].status == Status.blank.name

                if y != Field.y_cells - 1:
                    does_fit &= field_[x - 1][y + 1].status == Status.blank.name

            if y != 0:
                does_fit &= (field_[x][y - 1].status == Status.blank.name)

            if x != Field.x_cells - 1:
                does_fit &= (field_[x + 1][y].status == Status.blank.name)

                if y != 0:
                    does_fit &= field_[x + 1][y - 1].status == Status.blank.name

                if y != Field.y_cells - 1:
                    does_fit &= field_[x + 1][y + 1].status == Status.blank.name

            if y != Field.y_cells - 1:
                does_fit &= (field_[x][y + 1].status == Status.blank.name)

            does_fit &= field_[x][y].status == Status.blank.name

        return does_fit
