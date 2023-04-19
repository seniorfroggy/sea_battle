from src.Bot.Bot import *
from src.Player.Player import *
from src.Game.Game import *
from src.Field.Field import *
from src.Interface.Interface import *
from src.constants import DEFAULT_SIZE, GameStatus, LIST_OF_SHIPS


class System:

    def __init__(self):
        self.field = Field(self, DEFAULT_SIZE)
        self.interface = Interface(self)
        self.game = Game(GameStatus.prepare.name, LIST_OF_SHIPS, self)
        self.bot = Bot(self)
        self.player = Player(self)

    def get_bot(self):
        return self.bot

    def get_player(self):
        return self.player

    def get_field(self):
        return self.field

    def get_interface(self):
        return self.interface

    def get_game(self):
        return self.game
