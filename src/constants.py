from enum import Enum
LIST_OF_SHIPS = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
LIST_OF_SHIPS_REM = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
DEFAULT_ENEMY_SHIPS = [[[3, 0]], [[5, 8]], [[4, 5]], [[6, 2]], [[3, 2], [4, 2]], [[7, 8], [8, 8]],
                       [[8, 5], [9, 5]], [[0, 3], [0, 4], [0, 5]], [[2, 7], [2, 8], [2, 9]],
                       [[9, 0], [9, 1], [9, 2], [9, 3]]]
DEFAULT_SIZE = 10
MARGIN = 1 / 6
MAX_NUMBER_OF_RETRIES = 50
BOT_FIELD_SHIFT = 15


class Status(Enum):
    dead = "dead"
    alive = "alive"
    miss = "miss"
    blank = "blank"


class GameStatus(Enum):
    prepare = "prepare"
    finished = "finished"
    play = "play"
    finished_n_exit = "finished_exit"

