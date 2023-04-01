from constants import *
from class_Field.class_Cell.Cell import *

class Field:
    x_cells = DEFAULT_SIZE
    y_cells = DEFAULT_SIZE
    player_field = [[Cell("blank", [i, j], None) for j in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
    bot_field = [[Cell("blank", [i, j], None) for j in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]

    def __init__(self, sys):
        self.sys = sys

    def is_ship_destroyed(self, xc, yc):
        cnt = 0
        f = (self.bot_field if self.sys.get_game().player_turn else self.player_field)
        self.sys.get_tk().update()
        while xc + 1 < DEFAULT_SIZE and (f[xc + 1][yc].status == "alive" or f[xc + 1][yc].status == "dead"):
            cnt += (1 if f[xc + 1][yc].status == "alive" else 0)
            xc += 1
            self.sys.get_tk().update()
        while yc + 1 < DEFAULT_SIZE and (f[xc][yc + 1].status == "alive" or f[xc][yc + 1].status == "dead"):
            cnt += (1 if f[xc][yc + 1].status == "alive" else 0)
            yc += 1
            self.sys.get_tk().update()
        while xc - 1 >= 0 and (f[xc - 1][yc].status == "alive" or f[xc - 1][yc].status == "dead"):
            cnt += (1 if f[xc - 1][yc].status == "alive" else 0)
            xc -= 1
            self.sys.get_tk().update()
        while yc - 1 >= 0 and (f[xc][yc - 1].status == "alive" or f[xc][yc - 1].status == "dead"):
            cnt += (1 if f[xc][yc - 1].status == "alive" else 0)
            yc -= 1
            self.sys.get_tk().update()
        return cnt == 0

    def change_cell_status(self, xc, yc):
        flag = True
        if xc > 10 or yc > 10:
            flag = False
            if xc >= 10:
                xc = (xc - 1) % 10
            if yc >= 10:
                yc = (yc - 1) % 10

        if flag:
            if self.sys.get_field().player_field[xc][yc].status == "blank":
                self.sys.get_field().player_field[xc][yc].status = "miss"

                self.sys.get_interface().mark_as_miss(xc, yc)

                self.sys.get_game().player_turn = not self.sys.get_game().player_turn

            if self.sys.get_field().player_field[xc][yc].status == "alive":
                self.sys.get_field().player_field[xc][yc].status = "dead"
                self.sys.get_field().player_field[xc][yc].ship.hp -= 1

                self.sys.get_interface().draw_hit(xc, yc)

                if self.is_ship_destroyed(xc, yc):
                    self.sys.get_player().remaining_ships -= 1
                    self.player_field[xc][yc].ship.status = "dead"

                    self.sys.get_interface().change_number_of_ships()
        else:
            if self.sys.get_field().bot_field[xc][yc].status == "blank":
                self.sys.get_field().bot_field[xc][yc].status = "miss"

                self.sys.get_interface().mark_as_miss(xc + 11, yc + 11)

                self.sys.get_game().player_turn = not self.sys.get_game().player_turn

            if self.sys.get_field().bot_field[xc][yc].status == "alive":
                self.sys.get_field().bot_field[xc][yc].status = "dead"

                self.sys.get_interface().mark_as_hit(xc + 11, yc + 11)

                if self.is_ship_destroyed(xc, yc):
                    self.sys.get_bot().remaining_ships -= 1

    def does_ship_fit(self, coords, flag):
        if flag:
            f = self.sys.get_field().player_field
        else:
            f = self.sys.get_field().bot_field
        flag = True
        for xy in coords:
            x = xy[0]
            y = xy[1]
            flag &= ((0 <= x <= self.x_cells - 1) and (0 <= y <= self.y_cells - 1))
            if not flag:
                return False
            if x != 0:

                flag &= (f[x - 1][y].status == "blank")
                # print(x - 1, y, self.enemy_field[x - 1][y].status)
                # sys.stdout.flush()

                if y != 0:
                    flag &= f[x - 1][y - 1].status == "blank"
                    # print(x - 1, y - 1, self.enemy_field[x - 1][y - 1].status)
                    # sys.stdout.flush()

                if y != Field.y_cells - 1:
                    flag &= f[x - 1][y + 1].status == "blank"
                    # print(x - 1, y + 1, self.enemy_field[x - 1][y + 1].status)
                    # sys.stdout.flush()

            if y != 0:
                flag &= (f[x][y - 1].status == "blank")
                # print(x, y - 1, self.enemy_field[x][y - 1].status)
                # sys.stdout.flush()

            if x != Field.x_cells - 1:
                flag &= (f[x + 1][y].status == "blank")
                # print(x + 1, y, self.enemy_field[x + 1][y].status)
                # sys.stdout.flush()

                if y != 0:
                    flag &= f[x + 1][y - 1].status == "blank"
                    # print(x + 1, y - 1, self.enemy_field[x + 1][y - 1].status)
                    # sys.stdout.flush()

                if y != Field.y_cells - 1:
                    flag &= f[x + 1][y + 1].status == "blank"
                    # print(x + 1, y + 1, self.enemy_field[x + 1][y + 1].status)
                    # sys.stdout.flush()

            if y != Field.y_cells - 1:
                flag &= (f[x][y + 1].status == "blank")
                # print(x, y + 1, self.enemy_field[x][y + 1].status)
                # sys.stdout.flush()
            # print(x, y, self.enemy_field[x][y].status)
            # sys.stdout.flush()
            flag &= f[x][y].status == "blank"

        return flag