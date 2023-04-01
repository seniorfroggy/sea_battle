import time
from class_Bot.Bot import *
from class_Player.Player import *
from class_Game.Game import *
from class_Field.Field import *
from class_Interface.Interface import *

class System:
    tk = Tk()

    def __init__(self):
        self.tk.title("Sea Battle")
        self.tk.resizable(False, False)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=MyCanvas.size_x, height=MyCanvas.size_y, bd=0, highlightthickness=0)
        self.canvas.create_rectangle(0, 0, MyCanvas.size_x, MyCanvas.size_y, fill="black")
        self.canvas.pack()
        self.tk.update()
        self.field = Field(self)
        self.interface = Interface(self)
        self.interface.draw_field(0, 0)
        self.interface.draw_bot_field()
        self.game = Game("prepare", LIST_OF_SHIPS, self)
        self.tk.protocol("WM_DELETE_WINDOW", self.game.exiting)
        self.bot = Bot(self)
        self.player = Player(self)
        self.interface.draw_axes()
        self.interface.set_labels()

    def process(self):
        while self.game.status != "finished_exit":
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.005)

            if self.game.status == "prepare":
                if len(LIST_OF_SHIPS_REM) == 10:
                    self.interface.t1.place(x=self.interface.cell_size * (self.field.x_cells + 3), y=15)
            if self.game.status == "play":
                if not self.game.player_turn:
                    self.bot.make_shot()

    def bind_click(self):
        self.canvas.bind_all("<Button-1>", self.click)
        self.canvas.bind_all("<Button-3>", self.click)

    def click(self, event):
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        x = mouse_x // self.interface.cell_size
        y = mouse_y // self.interface.cell_size
        if self.game.status == "prepare":
            self.player.add_ship_position(x, y)
        elif self.game.status == "play":
            if event.num == 3:

                self.interface.mark_as_miss(x, y)

            else:
                self.game.make_shot(x, y)

    def get_bot(self):
        return self.bot

    def get_player(self):
        return self.player

    def get_field(self):
        return self.field

    def get_canvas(self):
        return self.canvas

    def get_tk(self):
        return self.tk

    def get_interface(self):
        return self.interface

    def get_game(self):
        return self.game