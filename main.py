from tkinter import *
import time
from tkinter import messagebox
from random import randrange
from constants import *


class Cell:
    coords = []
    status = "blank"
    ship = None

    def __init__(self, status, coords, ship):
        self.status = status
        self.coords = coords
        self.ship = ship


class Ship:

    def __init__(self, coords, status):
        self.coords = coords
        self.status = status
        self.hp = len(coords)


class MyCanvas:
    size_abscissa = 830
    size_ordinate = 830


class Bot:
    remaining_ships = 10
    ships = []

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

                if field.does_ship_fit(coords, False):
                    game.create_ship(coords, field.bot_field)
                    flag = True

                elif field.does_ship_fit(coords1, False):
                    game.create_ship(coords1, field.bot_field)
                    flag = True

                else:
                    retry_ += 1

        return True

    def make_shot(self):
        retry = 0

        x = randrange(0, DEFAULT_SIZE)
        y = randrange(0, DEFAULT_SIZE)

        while (field.player_field[x][y].status == "dead" or field.player_field[x][y].status == "miss") \
                and retry < 50:
            x = randrange(0, DEFAULT_SIZE)
            y = randrange(0, DEFAULT_SIZE)
            retry += 1
            tk.update()

        game.make_shot(x, y)


class Player:
    coords_container = []
    remaining_ships = 10
    ships = []

    def add_ship_position(self, xc, yc):

        self.coords_container.append([xc, yc])

        interface.draw_part_of_the_ship(xc, yc, [[1 / 6, 1 / 6], [1 / 6, 1 / 6]], "blue", "temp")

        if len(self.coords_container) == LIST_OF_SHIPS_REM[0]:

            if game.is_ship_valid(self.coords_container):
                game.create_ship(self.coords_container, field.player_field)
                LIST_OF_SHIPS_REM.pop(0)
                self.coords_container = []

                if not LIST_OF_SHIPS_REM:
                    game.start()
                    return

                interface.hide_t2_label()

                s = "Place {deck}-deck ship".format(deck=LIST_OF_SHIPS_REM[0])
                t1.configure(text=s)

            else:
                interface.delete_by_tag("temp")

                interface.show_t2_label()

                self.coords_container = []


class Game:
    player_turn = True

    def __init__(self, status, ships):
        self.status = status
        self.ships_to_place = ships

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
        return field.does_ship_fit(coords, True)

    def create_ship(self, coords, f):
        ship = Ship(coords, "alive")
        for i in range(len(coords)):
            xy = coords[i]
            f[xy[0]][xy[1]].status = "alive"
            f[xy[0]][xy[1]].ship = ship

        if f == field.player_field:
            interface.draw_ship(coords, "ally")
            player.ships.append(ship)
        else:
            bot.ships.append(ship)

    def start(self):
        interface.hide_t2_label()
        interface.delete_by_tag("temp")
        attempt = 0
        while not bot.generate_ships():
            attempt += 1
            if attempt > 1000:
                bot.ships = []
                for x_ in range(10):
                    for y_ in range(10):
                        field.bot_field[x_][y_].status = "blank"
                        field.bot_field[x_][y_].ship = None

                for coord in DEFAULT_ENEMY_SHIPS:
                    bot.ships.append(Ship(coord, "alive"))
                for item in bot.ships:
                    for xy in item.coords:
                        field.bot_field[xy[0]][xy[1]].status = "alive"
                break
        self.status = "play"
        t1.configure(foreground="black")
        interface.output_rules()

    def end(self):
        res = ("LOST!" if bot.remaining_ships != 0 else "WON!")
        color = ("red" if res == "LOST!" else "green")
        interface.draw_result(res, color)
        self.status = "finished"

    def make_shot(self, xc, yc):
        if (xc >= 10 >= yc) or (yc >= 10 >= xc) or (game.player_turn and (xc < 10 or yc < 10)):

            interface.show_t2_label()

            return

        interface.hide_t2_label()

        field.change_cell_status(xc, yc)

        self.check_game_finished()

    def check_game_finished(self):
        if bot.remaining_ships * player.remaining_ships == 0:
            self.end()

    @staticmethod
    def exiting():
        if messagebox.askokcancel("Exiting", "Wanna leave?"):
            game.status = "finished_exit"
            tk.destroy()


class Field:
    x_cells = DEFAULT_SIZE
    y_cells = DEFAULT_SIZE
    player_field = [[Cell("blank", [i, j], None) for j in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
    bot_field = [[Cell("blank", [i, j], None) for j in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]

    def is_ship_destroyed(self, xc, yc):
        cnt = 0
        f = (self.bot_field if game.player_turn else self.player_field)
        tk.update()
        while xc + 1 < DEFAULT_SIZE and (f[xc + 1][yc].status == "alive" or f[xc + 1][yc].status == "dead"):
            cnt += (1 if f[xc + 1][yc].status == "alive" else 0)
            xc += 1
            tk.update()
        while yc + 1 < DEFAULT_SIZE and (f[xc][yc + 1].status == "alive" or f[xc][yc + 1].status == "dead"):
            cnt += (1 if f[xc][yc + 1].status == "alive" else 0)
            yc += 1
            tk.update()
        while xc - 1 >= 0 and (f[xc - 1][yc].status == "alive" or f[xc - 1][yc].status == "dead"):
            cnt += (1 if f[xc - 1][yc].status == "alive" else 0)
            xc -= 1
            tk.update()
        while yc - 1 >= 0 and (f[xc][yc - 1].status == "alive" or f[xc][yc - 1].status == "dead"):
            cnt += (1 if f[xc][yc - 1].status == "alive" else 0)
            yc -= 1
            tk.update()
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
            if field.player_field[xc][yc].status == "blank":
                field.player_field[xc][yc].status = "miss"

                interface.mark_as_miss(xc, yc)

                game.player_turn = not game.player_turn

            if field.player_field[xc][yc].status == "alive":
                field.player_field[xc][yc].status = "dead"
                field.player_field[xc][yc].ship.hp -= 1

                interface.draw_hit(xc, yc)

                if self.is_ship_destroyed(xc, yc):
                    player.remaining_ships -= 1
                    self.player_field[xc][yc].ship.status = "dead"

                    interface.change_number_of_ships()
        else:
            if field.bot_field[xc][yc].status == "blank":
                field.bot_field[xc][yc].status = "miss"

                interface.mark_as_miss(xc + 11, yc + 11)

                game.player_turn = not game.player_turn

            if field.bot_field[xc][yc].status == "alive":
                field.bot_field[xc][yc].status = "dead"

                interface.mark_as_hit(xc + 11, yc + 11)

                if self.is_ship_destroyed(xc, yc):
                    bot.remaining_ships -= 1

    def does_ship_fit(self, coords, flag):
        if flag:
            f = field.player_field
        else:
            f = field.bot_field
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


class Interface:
    cell_size = MyCanvas.size_abscissa // (2 * DEFAULT_SIZE + 1)

    def draw_part_of_the_ship(self, xc, yc, shift, color, tag):
        canvas.create_rectangle(xc * self.cell_size, yc * self.cell_size,
                                xc * self.cell_size + self.cell_size,
                                yc * self.cell_size + self.cell_size, fill=color,
                                tags=tag)
        canvas.create_rectangle((xc + shift[0][0]) * self.cell_size, (yc + shift[0][1]) * self.cell_size,
                                (xc - shift[1][0]) * self.cell_size + self.cell_size,
                                (yc - shift[1][1]) * self.cell_size + self.cell_size, fill="black",
                                tags=tag)

    def draw_ship(self, coords, f):
        for i in range(len(coords)):
            xy = coords[i]
            xc = xy[0]
            yc = xy[1]
            if f == "bot":
                xc += 11
                yc += 11
            shift = [[1 / 6, 1 / 6], [1 / 6, 1 / 6]]
            if 0 < i < len(coords) - 1:
                direction = coords[i][0] == coords[i - 1][0]
                shift[0][direction] = -1 / 6
                shift[1][direction] = -1 / 6
            elif i == 0 and i < len(coords) - 1:
                direction = coords[i][0] == coords[i + 1][0]
                shift[1][direction] = -1 / 6
            elif 0 < i == len(coords) - 1:
                direction = coords[i][0] == coords[i - 1][0]
                shift[0][direction] = -1 / 6

            if f != "bot":
                color = ("white" if field.player_field[xc][yc].status == "alive" else "#90021f")
            else:
                color = ("white" if field.bot_field[xc - 11][yc - 11].status == "alive" else "#90021f")

            self.draw_part_of_the_ship(xc, yc, shift, color, "tag{xt}{yt}".format(xt=xc, yt=yc))

            if color == "#90021f":
                self.mark_as_hit(xc, yc)

    def mark_as_miss(self, xc, yc):
        canvas.create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='M'), font=("nosans", 15), fill="white", tags="M")

    def draw_hit(self, xc, yc):
        self.delete_by_tag("tag{xt}{yt}".format(xt=xc, yt=yc))

        self.draw_ship(field.player_field[xc][yc].ship.coords, "ally")

        canvas.create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='X'), font=("nosans", 15), fill="white", tags="X")

    def mark_as_hit(self, xc, yc):
        color = "#90021f"
        if xc < 10 and yc < 10:
            color = "white"
        canvas.create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='X'), font=("nosans", 15), fill=color, tags="X")

    def change_number_of_ships(self):
        self.delete_by_tag("ally_ships")
        canvas.create_text(self.cell_size * (field.x_cells + 6), 154,
                           text="You have {num} ships left".format(num=player.remaining_ships),
                           fill="white", font=("nosans", 16), width=300, tags="ally_ships")

    def draw_axes(self):
        for i in range(Field.x_cells):
            canvas.create_text(interface.cell_size * (field.x_cells + 0.5), i * interface.cell_size + 15,
                               text="{let}".format(let=LETTERS[i]), font=("Times", 15), fill="white")
            canvas.create_text(interface.cell_size * (field.x_cells + 0.5), (i + 11) * interface.cell_size + 15,
                               text="{let}".format(let=LETTERS[i]), font=("Times", 15), fill="white")
            canvas.create_text(i * interface.cell_size + 15, interface.cell_size * (field.y_cells + 0.5),
                               text="{num}".format(num=i + 1), font=("Times", 15), fill="white")
            canvas.create_text((i + 11) * interface.cell_size + 15, interface.cell_size * (field.y_cells + 0.5),
                               text="{num}".format(num=i + 1), font=("Times", 15), fill="white")

    def draw_bot_ships(self):
        for ship in bot.ships:
            self.draw_ship(ship.coords, "bot")

    def draw_bot_field(self):
        start_x = interface.cell_size * (field.x_cells + 1)
        start_y = interface.cell_size * (field.y_cells + 1)
        self.draw_field(start_x, start_y)

    def draw_field(self, shift_x, shift_y):
        for i in range(0, field.x_cells + 1):
            canvas.create_line(shift_x + Interface.cell_size * i, shift_y,
                               shift_x + Interface.cell_size * i, shift_y + field.y_cells * Interface.cell_size,
                               fill="white", width=2)
        for i in range(0, field.y_cells + 1):
            canvas.create_line(shift_x, shift_y + Interface.cell_size * i,
                               shift_x + field.x_cells * Interface.cell_size, shift_y + Interface.cell_size * i,
                               fill="violet", width=2)

    def draw_result(self, text, color):
        t0 = Label(text="YOU'VE {t}".format(t=text), foreground=color, font=("nos ans", 50), background="black")
        t0.place(x=interface.cell_size * 5, y=self.cell_size * 7)
        self.draw_bot_ships()
        self.delete_by_tag("M", "X", "tag3", "tag2", "ally_ships")

    def show_t2_label(self):
        t2.configure(foreground="white")
        t2.place(x=self.cell_size * (field.x_cells + 3), y=50)

    def hide_t2_label(self):
        t2.configure(foreground="black")
        t2.place(x=interface.cell_size * (field.x_cells + 3), y=50)

    def output_rules(self):
        canvas.create_text(interface.cell_size * (field.x_cells + 6), 100,
                           text="1. 'M' stands for 'MISS'",
                           fill="white", font=("nosans", 16), width=300, tags="tag3")

        canvas.create_text(interface.cell_size * (field.x_cells + 6), 127,
                           text="2. 'X' means hit",
                           fill="white", font=("nosans", 16), width=300, tags="tag2")
        canvas.create_text(interface.cell_size * (field.x_cells + 6), 154,
                           text="U have {num} ships left".format(num=player.remaining_ships),
                           fill="white", font=("nosans", 16), width=300, tags="ally_ships")

    def delete_by_tag(self, *tags):
        for tag in tags:
            canvas.delete(tag)




def click(event):

    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    x = mouse_x // interface.cell_size
    y = mouse_y // interface.cell_size
    if game.status == "prepare":
        player.add_ship_position(x, y)
    elif game.status == "play":
        if event.num == 3:

            interface.mark_as_miss(x, y)

        else:
            game.make_shot(x, y)


if __name__ == "__main__":

    tk = Tk()
    tk.protocol("WM_DELETE_WINDOW", Game.exiting)
    tk.title("Sea Battle")
    tk.resizable(False, False)
    tk.wm_attributes("-topmost", 1)

    canvas = Canvas(tk, width=MyCanvas.size_abscissa, height=MyCanvas.size_ordinate, bd=0, highlightthickness=0)
    canvas.create_rectangle(0, 0, MyCanvas.size_abscissa, MyCanvas.size_ordinate, fill="black")
    canvas.pack()
    tk.update()

    field = Field()
    interface = Interface()
    interface.draw_field(0, 0)
    interface.draw_bot_field()

    game = Game("prepare", LIST_OF_SHIPS)

    bot = Bot()
    player = Player()
    interface.draw_axes()

    canvas.bind_all("<Button-1>", click)
    canvas.bind_all("<Button-3>", click)

    t1 = Label(tk, text="Place 1-deck ship", font=("nos ans", 16), background="black", foreground="white")
    string = "Invalid position, try again!".format(deck=LIST_OF_SHIPS_REM[0])
    t2 = Label(tk, text=string, font=("nos ans", 16), background="black", foreground="white")

    while game.status != "finished_exit":
        tk.update_idletasks()
        tk.update()
        time.sleep(0.005)

        if game.status == "prepare":
            if len(LIST_OF_SHIPS_REM) == 10:
                t1.place(x=interface.cell_size * (field.x_cells + 3), y=15)
        if game.status == "play":
            if not game.player_turn:
                bot.make_shot()
