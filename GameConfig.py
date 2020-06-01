from enum import Enum


# Clase con la configuración del juego
class GameConfig:
    def __init__(self):
        """
        Init function
        Set variables to privates to use getters and setters.
        """
        # La matriz del juego
        self.__matrix = []
        # El modo del juego, por defecto en alfabético
        self.__game_mode = GameModes.ALPHA
        # El tamaño de la matriz del juego, debe ser cuadrada
        self.__matrix_size = 0
        # La puntuación del juego
        self.__record = 0
        # Los movimientos del juego
        self.__moves = 0
        # El número de obstáculos de la matriz
        self.__obstacles = 0

    def get_matrix(self):
        """
        Devuelve la matriz del juego
        :return: la matriz del juego
        """
        return self.__matrix

    def set_matrix(self, new_matrix):
        """
        Da nuevo valor a la matriz del juego
        :param new_matrix: la nueva matriz
        :return: None
        """
        self.__matrix = new_matrix
        return None

    def get_matrix_size(self):
        """
        Devuelve El tamaño de la matriz del juego
        :return:
        """
        return self.__matrix_size

    def set_matrix_size(self, new_size):
        """
        Da nuevo valor al tamaño de la matriz del juego, que deberá ser cuadrada
        :param new_size: el nuevo tamaño de la nueva matriz
        :return: None
        """
        self.__matrix_size = new_size
        # Inicializamos la matriz
        self.set_matrix([[" "] * self.__matrix_size for i in range(self.__matrix_size)])
        return None

    def get_obstacles(self):
        """
        Devuelve el número de los obstáculos de la matriz
        :return: El número de obstáculos de la matriz
        """
        return self.__obstacles

    def set_obstacles(self, new_value):
        """
        Da nuevo valor al número de obstáculos de la matriz
        :param new_value: el nuevo número de obstaculos de la matriz
        :return: None
        """
        self.__obstacles = new_value
        return None

    def get_moves(self):
        """
        Devuelve los movimientos realizados por el jugador
        :return: los movimientos realizados por el jugador
        """
        return self.__moves

    def set_moves(self, new_value):
        """
        Da nuevo valor a los movimientos realizados por el jugador
        :param new_value: el nuevo valor
        :return: None
        """
        self.__moves = new_value
        return None

    def get_record(self):
        """
        Devuelve la puntuación conseguida por el jugador hasta el momento
        :return: la puntuación conseguida por el jugador hasta el momento
        """
        return self.__record

    def set_record(self, new_value):
        """
        Da nuevo valor a la puntuación conseguida por el jugador
        :param new_value: la nueva puntuación
        :return: None
        """
        self.__record = new_value
        return None

    def get_mode(self):
        """
        Devuelve el modo del tablero del juego
        :return: el modo del tablero del juego
        """
        return self.__game_mode

    def set_mode(self, new_mode):
        """
        Da nuevo valor al modo del tablero del juego
        :param new_mode: el nuevo modo
        :return: None
        """
        self.__game_mode = new_mode
        return None


# los distintos modos del juego
class GameModes(Enum):
    ALPHA = 1  # Alfabético
    LEVEL = 2  # Nivel
    A = 3  # 1024
    B = 4  # 2048


# Los distintos movimientos del juego
class GameMovements(Enum):
    UP = 1  # ARRIBA
    DOWN = 2  # ABAJO
    LEFT = 3  # IZQUIERDA
    RIGHT = 4  # DERECHA
