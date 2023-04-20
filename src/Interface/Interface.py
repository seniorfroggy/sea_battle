import time
import pygame

from src.Interface.MyCanvas.MyCanvas import MyCanvas
from src.constants import DEFAULT_SIZE, MARGIN, LETTERS, LIST_OF_SHIPS_REM, Status, GameStatus, BOT_FIELD_SHIFT
from tkinter import *
from src.Graphics_constants import *
from tkinter import messagebox


class Interface:
    cell_size = 2 * MyCanvas.size_y // (3 * DEFAULT_SIZE)
    tk = Tk()

    shift_x_player_field = MyCanvas.size_x // 12
    shift_y_player_field = MyCanvas.size_y // 6

    shift_x_bot_field = 7 * cell_size * DEFAULT_SIZE // 4
    shift_y_bot_field = shift_y_player_field

    def __init__(self, sys):
        self.main_label = Label()
        self.warning_label = Label()
        self.sys = sys
        pygame.mixer.init()
        self.__init_tk__()
        self.__init_canvas__()
        self.prepare_for_start()

    def prepare_for_start(self):
        """this func draws all field elements and loads to soundtracks"""
        self.draw_field(self.shift_x_player_field, self.shift_y_player_field, True)
        self.draw_bot_field()
        self.draw_axes()
        self.set_labels()
        pygame.mixer.music.load("src/music/preparing_sound.mp3")
        pygame.mixer.music.load("src/music/pirates2.mp3")
        self.play_sound("src/music/preparing_sound.mp3")

    def __init_canvas__(self):
        """this func initializes canvas subclass"""
        self.canvas = Canvas(self.tk, width=MyCanvas.size_x, height=MyCanvas.size_y, bd=0, highlightthickness=0)
        self.canvas.create_rectangle(0, 0, MyCanvas.size_x, MyCanvas.size_y, fill="black")
        self.canvas.pack()

    def __init_tk__(self):
        """this func initializes tk subclass"""
        self.tk.title("Sea Battle")
        self.tk.resizable(False, False)
        self.tk.wm_attributes("-topmost", 1)
        self.tk.update()
        self.tk.protocol("WM_DELETE_WINDOW", self.exiting)

    def bind_click(self):
        """this func binds click event"""
        self.canvas.bind_all("<Button-1>", self.click)
        self.canvas.bind_all("<Button-3>", self.click)

    def click(self, event):
        """this func calls add_ship_position(x, y)/make_shot(x, y)/mark_as_miss(x, y) depending on the game status"""
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        x = (mouse_x - self.shift_x_player_field) // self.cell_size
        y = (mouse_y - self.shift_y_player_field) // self.cell_size
        if self.sys.get_game().status == GameStatus.prepare.name:
            self.sys.get_player().add_ship_position(x, y)

        elif self.sys.get_game().status == GameStatus.play.name:
            if event.num == 3:
                self.mark_as_miss(x, y)
            else:
                if self.sys.get_game().player_turn:
                    self.sys.get_game().make_shot(x, y)

    def process(self):
        """this func represents event loop and calls make_shot()/main_label.place() depending on the game status"""
        while self.sys.get_game().status != GameStatus.finished_n_exit.name:
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.005)

            if self.sys.get_game().status == GameStatus.prepare.name:
                if len(LIST_OF_SHIPS_REM) == 10:
                    self.sys.get_interface().main_label.place(x=self.sys.get_interface().cell_size *
                                                              (DEFAULT_SIZE + 3), y=15)
            if self.sys.get_game().status == GameStatus.play.name:
                if not self.sys.get_game().player_turn:
                    self.sys.get_bot().make_shot()

    def draw_part_of_the_ship(self, xc, yc, shift, color, tag):
        """this func draws part of the ship using provided arguments"""
        self.canvas.create_rectangle(self.shift_x_player_field + xc * self.cell_size,
                                     self.shift_y_player_field + yc * self.cell_size,
                                     self.shift_x_player_field + xc * self.cell_size + self.cell_size,
                                     self.shift_y_player_field + yc * self.cell_size + self.cell_size, fill=color,
                                     tags=tag)
        self.canvas.create_rectangle(self.shift_x_player_field + (xc + shift[0][0]) * self.cell_size,
                                     self.shift_y_player_field + (yc + shift[0][1]) * self.cell_size,
                                     self.shift_x_player_field + (xc - shift[1][0]) * self.cell_size + self.cell_size,
                                     self.shift_y_player_field + (yc - shift[1][1]) * self.cell_size + self.cell_size,
                                     fill=BACKGROUND_COLOUR,
                                     tags=tag)

    def draw_ship(self, coords, on_ally_field):
        """this func generates arguments to call draw_part_of_the_ship(*args)"""
        for i in range(len(coords)):
            xy = coords[i]
            xc = xy[0]
            yc = xy[1]
            if not on_ally_field:
                xc += BOT_FIELD_SHIFT
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

            if on_ally_field:
                color = (SHIP_COLOUR if self.sys.get_field().player_field[xc][yc].status == Status.alive.name
                         else DEAD_SHIP_COLOUR)
            else:
                color = (SHIP_COLOUR if self.sys.get_field().bot_field[xc - BOT_FIELD_SHIFT][yc].status == Status.alive.name
                         else DEAD_SHIP_COLOUR)

            self.draw_part_of_the_ship(xc, yc, shift, color, "tag{xt}{yt}".format(xt=xc, yt=yc))

            if color == DEAD_SHIP_COLOUR:
                self.mark_as_hit(xc, yc)

    def mark_as_miss(self, xc, yc):
        """this func marks given cell as a miss"""
        self.canvas.create_text(self.shift_x_player_field + self.cell_size * (xc + 0.5),
                                self.shift_y_player_field + self.cell_size * (yc + 0.5),
                                text=MISS_MARK, font=(BASE_FONT, 15), fill=TEXT_COLOUR, tags=MISS_MARK)

    def draw_hit(self, xc, yc):
        """this func draws a hit on the part of the ship"""
        self.delete_by_tag("tag{xt}{yt}".format(xt=xc, yt=yc))

        self.draw_ship(self.sys.get_field().player_field[xc][yc].ship.coords, True)

        self.canvas.create_text(self.shift_x_player_field + self.cell_size * (xc + 0.5),
                                self.shift_y_player_field + self.cell_size * (yc + 0.5),
                                text=HIT_MARK, font=(BASE_FONT, 15), fill=TEXT_COLOUR, tags=HIT_MARK)

    def mark_as_hit(self, xc, yc):
        """this func marks given cell as hit"""
        color = PLAYER_HIT_COLOUR
        if xc < 10 and yc < 10:
            color = MISS_COLOUR
        self.canvas.create_text(self.shift_x_player_field + self.cell_size * (xc + 0.5),
                                self.shift_y_player_field + self.cell_size * (yc + 0.5),
                                text=HIT_MARK, font=(BASE_FONT, 15), fill=color, tags=HIT_MARK)

    def change_number_of_ships(self):
        self.delete_by_tag("ally_ships")

    def draw_axes(self):
        """this func draws player's and bot's axes"""
        for i in range(DEFAULT_SIZE):
            self.canvas.create_text(self.shift_x_player_field + self.cell_size *
                                    DEFAULT_SIZE + self.cell_size / 2,
                                    self.shift_y_player_field + i * self.cell_size + self.cell_size / 2,
                                    text="{let}".format(let=LETTERS[i]), font=(AXES_FONT, 15), fill=AXES_COLOUR)
            self.canvas.create_text(self.shift_x_bot_field + self.cell_size *
                                    DEFAULT_SIZE + self.cell_size / 2,
                                    self.shift_y_bot_field + i * self.cell_size + self.cell_size / 2,
                                    text="{let}".format(let=LETTERS[i]), font=(AXES_FONT, 15), fill=AXES_COLOUR)
            self.canvas.create_text(self.shift_x_player_field + i * self.cell_size + self.cell_size / 2,
                                    self.shift_y_player_field + self.cell_size *
                                    self.sys.get_field().y_cells + self.cell_size / 2,
                                    text="{num}".format(num=i + 1), font=(AXES_FONT, 15), fill=AXES_COLOUR)
            self.canvas.create_text(self.shift_x_bot_field + i *
                                    self.cell_size + self.cell_size / 2,
                                    self.shift_y_bot_field + self.cell_size *
                                    self.sys.get_field().y_cells + self.cell_size / 2,
                                    text="{num}".format(num=i + 1), font=(AXES_FONT, 15), fill=AXES_COLOUR)

    def draw_bot_ships(self):
        """this func draws bot's ship using above-mentioned draw_ship()"""
        for ship in self.sys.get_bot().ships:
            self.draw_ship(ship.coords, False)

    def draw_bot_field(self):
        """this func draws bot's field using draw_field()"""
        self.draw_field(self.shift_x_bot_field, self.shift_y_bot_field, False)

    def draw_field(self, shift_x, shift_y, on_player_field):
        """this func draws bot's/player's field"""
        if on_player_field:
            vertical_color = WHITE_COLOUR
            horizontal_color = [MAGENTA_COLOUR, MEDIUMPURPLE_COLOUR, BLUEVIOLET_COLOUR,
                                DARKVIOLET_COLOUR, DARKMAGENTA_COLOUR, VIOLET_COLOUR]
        else:
            vertical_color = WHITE_COLOUR
            horizontal_color = [ORANGERED_COLOUR, CORAL_COLOR, DARKORANGE_COLOUR,
                                TOMATO_COLOUR, ORANGE_COLOUR, LIGHTSALMON_COLOUR]

        for i in range(0, DEFAULT_SIZE + 1):
            self.canvas.create_line(shift_x + Interface.cell_size * i, shift_y,
                                    shift_x + Interface.cell_size * i,
                                    shift_y + self.sys.get_field().y_cells * Interface.cell_size,
                                    fill=vertical_color, width=2)
        for i in range(0, self.sys.get_field().y_cells + 1):
            self.canvas.create_line(shift_x, shift_y + Interface.cell_size * i,
                                    shift_x + DEFAULT_SIZE * Interface.cell_size,
                                    shift_y + Interface.cell_size * i,
                                    fill=horizontal_color[i // 2], width=2)

    def output_result(self, text, color):
        """this func outputs results of the game"""
        t0 = Label(text="YOU'VE {t}".format(t=text), foreground=color,
                   font=(BASE_FONT, 50), background=BACKGROUND_COLOUR)
        t0.place(x=self.sys.get_interface().cell_size * 10, y=self.cell_size * 7)
        if text == "LOST!":
            self.play_endgame_sound("src/music/babahz.mp3")
        else:
            self.play_endgame_sound("src/music/win_sound.mp3")
        self.draw_bot_ships()
        self.delete_by_tag(MISS_MARK, HIT_MARK, "tag3", "tag2", "ally_ships")

    def show_warning(self):
        """this func shows label containnig a warning"""
        self.warning_label.configure(foreground=TEXT_COLOUR)
        self.warning_label.place(x=self.cell_size * (DEFAULT_SIZE + 3), y=50)

    def hide_warning(self):
        """this func hides label containnig a warning"""
        self.warning_label.configure(foreground=BACKGROUND_COLOUR)
        self.warning_label.place(x=self.cell_size * (DEFAULT_SIZE + 3), y=50)

    def output_rules(self):
        """this func outputs text with the game rules"""
        self.canvas.create_text(self.cell_size * (DEFAULT_SIZE - 3), MyCanvas.size_y / 12,
                                text="1. 'M' stands for 'MISS'",
                                fill=TEXT_COLOUR, font=(BASE_FONT, 16), width=300, tags="tag3")

        self.canvas.create_text(self.cell_size * (DEFAULT_SIZE + 12), MyCanvas.size_y / 12,
                                text="2. 'X' means hit",
                                fill=TEXT_COLOUR, font=(BASE_FONT, 16), width=300, tags="tag2")

    def delete_by_tag(self, *tags):
        """this func deletes all texts with the tag from arguments"""
        for tag in tags:
            self.canvas.delete(tag)

    def set_labels(self):
        """this func sets two main labels"""
        self.main_label = Label(self.tk, text="Place 1-deck ship",
                                font=(BASE_FONT, 16), background=BACKGROUND_COLOUR, foreground=TEXT_COLOUR)
        string = "Invalid position, try again!".format(deck=LIST_OF_SHIPS_REM[0])
        self.warning_label = Label(self.tk, text=string,
                                   font=(BASE_FONT, 16), background=BACKGROUND_COLOUR, foreground=TEXT_COLOUR)

    def exiting(self):
        """this func exits the game"""
        if messagebox.askokcancel("Exiting", "Wanna leave?"):
            self.sys.get_game().status = GameStatus.finished_n_exit.name
            self.tk.destroy()

    @staticmethod
    def play_endgame_sound(file):
        """this func stops all Channels and plays a given file"""
        pygame.mixer.Channel(0).stop()
        pygame.mixer.music.load(file)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(file))

    @staticmethod
    def play_sound(file):
        """this func plays given file"""
        pygame.mixer.Channel(0).set_volume(0.4)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(file), loops=-1)

    @staticmethod
    def play_temp_sound(file, pause):
        """this func fades background sound a then plays given file"""
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.music.load(file)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(file))
        time.sleep(pause)
        pygame.mixer.Channel(0).set_volume(0.4)