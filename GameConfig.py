from enum import Enum


class GameConfig:
    def __init__(self):
        """
        Init function
        Set variables to privates to use getters and setters.
        """
        self.__matrix = []
        self.__game_mode = GameModes.ALPHA
        self.__matrix_size = 0
        self.__file_path = ""
        self.__record = 0
        self.__moves = 0
        self.__obstacles = 0

    def get_matrix(self):
        return self.__matrix

    def set_matrix(self, new_matrix):
        self.__matrix = new_matrix
        return None

    def get_matrix_size(self):
        return self.__matrix_size

    def set_matrix_size(self, new_size):
        self.__matrix_size = new_size
        if len(self.__matrix) == 0:
            self.set_matrix([[" "] * self.__matrix_size for i in range(self.__matrix_size)])
        return None

    def get_obstacles(self):
        return self.__obstacles

    def set_obstacles(self, new_value):
        self.__obstacles = new_value
        return None

    def get_moves(self):
        return self.__moves

    def set_moves(self, new_value):
        self.__moves = new_value
        return None

    def get_record(self):
        return self.__moves

    def set_record(self, new_value):
        self.__record = new_value
        return None

    def get_mode(self):
        return self.__game_mode

    def set_mode(self, new_mode):
        self.__game_mode = new_mode
        return None


class GameModes(Enum):
    ALPHA = 1
    LEVEL = 2
    A = 3
    B = 4


class GameMovements(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
