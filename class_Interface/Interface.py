from constants import *
from class_Interface.class_MyCanvas.MyCanvas import *
from tkinter import *

class Interface:
    cell_size = MyCanvas.size_x // (2 * DEFAULT_SIZE + 1)

    def __init__(self, sys):
        self.t1 = Label()
        self.t2 = Label()
        self.sys = sys

    def draw_part_of_the_ship(self, xc, yc, shift, color, tag):
        self.sys.canvas.create_rectangle(xc * self.cell_size, yc * self.cell_size,
                                xc * self.cell_size + self.cell_size,
                                yc * self.cell_size + self.cell_size, fill=color,
                                tags=tag)
        self.sys.canvas.create_rectangle((xc + shift[0][0]) * self.cell_size, (yc + shift[0][1]) * self.cell_size,
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
            shift = [[MARGIN, MARGIN], [MARGIN, MARGIN]]
            if 0 < i < len(coords) - 1:
                direction = coords[i][0] == coords[i - 1][0]
                shift[0][direction] = -MARGIN
                shift[1][direction] = -MARGIN
            elif i == 0 and i < len(coords) - 1:
                direction = coords[i][0] == coords[i + 1][0]
                shift[1][direction] = -MARGIN
            elif 0 < i == len(coords) - 1:
                direction = coords[i][0] == coords[i - 1][0]
                shift[0][direction] = -MARGIN

            if f != "bot":
                color = ("white" if self.sys.get_field().player_field[xc][yc].status == "alive" else "#90021f")
            else:
                color = ("white" if self.sys.get_field().bot_field[xc - 11][yc - 11].status == "alive" else "#90021f")

            self.draw_part_of_the_ship(xc, yc, shift, color, "tag{xt}{yt}".format(xt=xc, yt=yc))

            if color == "#90021f":
                self.mark_as_hit(xc, yc)

    def mark_as_miss(self, xc, yc):
        self.sys.get_canvas().create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='M'), font=("nosans", 15), fill="white", tags="M")

    def draw_hit(self, xc, yc):
        self.delete_by_tag("tag{xt}{yt}".format(xt=xc, yt=yc))

        self.draw_ship(self.sys.get_field().player_field[xc][yc].ship.coords, "ally")

        self.sys.get_canvas().create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='X'), font=("nosans", 15), fill="white", tags="X")

    def mark_as_hit(self, xc, yc):
        color = "#90021f"
        if xc < 10 and yc < 10:
            color = "white"
        self.sys.get_canvas().create_text(self.cell_size * (xc + 0.5), self.cell_size * (yc + 0.5),
                           text="{let}".format(let='X'), font=("nosans", 15), fill=color, tags="X")

    def change_number_of_ships(self):
        self.delete_by_tag("ally_ships")
        self.sys.get_canvas().create_text(self.cell_size * (self.sys.get_field().x_cells + 6), 154,
                           text="You have {num} ships left".format(num=self.sys.get_player().remaining_ships),
                           fill="white", font=("nosans", 16), width=300, tags="ally_ships")

    def draw_axes(self):
        for i in range(self.sys.get_field().x_cells):
            self.sys.get_canvas().create_text(self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 0.5),
                               i * self.sys.get_interface().cell_size + 15,
                               text="{let}".format(let=LETTERS[i]), font=("Times", 15), fill="white")
            self.sys.get_canvas().create_text(self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 0.5),
                               (i + 11) * self.sys.get_interface().cell_size + 15,
                               text="{let}".format(let=LETTERS[i]), font=("Times", 15), fill="white")
            self.sys.get_canvas().create_text(i * self.sys.get_interface().cell_size + 15,
                               self.sys.get_interface().cell_size * (self.sys.get_field().y_cells + 0.5),
                               text="{num}".format(num=i + 1), font=("Times", 15), fill="white")
            self.sys.get_canvas().create_text((i + 11) * self.sys.get_interface().cell_size + 15,
                               self.sys.get_interface().cell_size * (self.sys.get_field().y_cells + 0.5),
                               text="{num}".format(num=i + 1), font=("Times", 15), fill="white")

    def draw_bot_ships(self):
        for ship in self.sys.get_bot().ships:
            self.draw_ship(ship.coords, "bot")

    def draw_bot_field(self):
        start_x = self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 1)
        start_y = self.sys.get_interface().cell_size * (self.sys.get_field().y_cells + 1)
        self.draw_field(start_x, start_y)

    def draw_field(self, shift_x, shift_y):
        for i in range(0, self.sys.get_field().x_cells + 1):
            self.sys.get_canvas().create_line(shift_x + Interface.cell_size * i, shift_y,
                               shift_x + Interface.cell_size * i, shift_y + self.sys.get_field().y_cells * Interface.cell_size,
                               fill="white", width=2)
        for i in range(0, self.sys.get_field().y_cells + 1):
            self.sys.get_canvas().create_line(shift_x, shift_y + Interface.cell_size * i,
                               shift_x + self.sys.get_field().x_cells * Interface.cell_size, shift_y + Interface.cell_size * i,
                               fill="violet", width=2)

    def draw_result(self, text, color):
        t0 = Label(text="YOU'VE {t}".format(t=text), foreground=color, font=("nos ans", 50), background="black")
        t0.place(x=self.sys.get_interface().cell_size * 5, y=self.cell_size * 7)
        self.draw_bot_ships()
        self.delete_by_tag("M", "X", "tag3", "tag2", "ally_ships")

    def show_t2_label(self):
        self.sys.get_interface().t2.configure(foreground="white")
        self.sys.get_interface().t2.place(x=self.cell_size * (self.sys.get_field().x_cells + 3), y=50)

    def hide_t2_label(self):
        self.sys.get_interface().t2.configure(foreground="black")
        self.sys.get_interface().t2.place(x=self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 3), y=50)

    def output_rules(self):
        self.sys.get_canvas().create_text(self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 6), 100,
                           text="1. 'M' stands for 'MISS'",
                           fill="white", font=("nosans", 16), width=300, tags="tag3")

        self.sys.get_canvas().create_text(self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 6), 127,
                           text="2. 'X' means hit",
                           fill="white", font=("nosans", 16), width=300, tags="tag2")
        self.sys.get_canvas().create_text(self.sys.get_interface().cell_size * (self.sys.get_field().x_cells + 6), 154,
                           text="U have {num} ships left".format(num=self.sys.get_player().remaining_ships),
                           fill="white", font=("nosans", 16), width=300, tags="ally_ships")

    def delete_by_tag(self, *tags):
        for tag in tags:
            self.sys.get_canvas().delete(tag)

    def set_labels(self):
        self.sys.get_interface().t1 = Label(self.sys.get_tk(), text="Place 1-deck ship", font=("nos ans", 16), background="black", foreground="white")
        string = "Invalid position, try again!".format(deck=LIST_OF_SHIPS_REM[0])
        self.sys.get_interface().t2 = Label(self.sys.get_tk(), text=string, font=("nos ans", 16), background="black", foreground="white")