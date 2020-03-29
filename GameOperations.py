import random

from functools import reduce

from GameConfig import GameModes


def create_random_obstacles(matrix, n):
    """
    Creación de nuevos obstáculos aleatorios
    :param matrix: la matriz del juego
    :param n: el número de obstaculos
    :return: None si n == 0
    """
    if n == 0:
        return None
    empty_position = random_empty_space_position(matrix)
    matrix[empty_position[0]][empty_position[1]] = "*"
    return create_random_obstacles(matrix, n - 1)


def random_empty_space_position(matrix):
    """
    Obtención de una posición aleatoria en blanco
    :param matrix: la matriz del juego
    :return: (fila, columna) posición del espacio en blanco
    """
    matrix_empty_spaces = get_matrix_empty_spaces(matrix)
    # https://stackoverflow.com/questions/2844516/how-to-filter-a-dictionary-according-to-an-arbitrary-condition-function
    filtered = {k: v for k, v in matrix_empty_spaces.items() if len(v) > 0}
    # https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary-in-python
    row, columns = random.choice(list(filtered.items()))
    _random_number = random_number(0, len(columns))
    column = columns[_random_number]
    print("row : " + str(row) + " column : " + str(column))
    return row, column


def total_matrix_empty_spaces(matrix_empty_spaces):
    filtered = {k: v for k, v in matrix_empty_spaces.items() if len(v) > 0}
    empty_spaces_list = list(map(lambda k: len(k[1]), list(filtered.items())))
    return reduce((lambda x, y: x + y), empty_spaces_list)


def insert_new_block(matrix, game_mode):
    probability = (1, 1, 1, 2)
    level = probability[random_number(0, len(probability))]
    position = random_empty_space_position(matrix)
    if level == 1:
        if game_mode == GameModes.ALPHA:
            matrix[position[0]][position[1]] = "A"
    else:
        if game_mode == GameModes.ALPHA:
            matrix[position[0]][position[1]] = "B"
    return None


def is_possible_move(matrix):
    filtered = {k: v for k, v in get_matrix_empty_spaces(matrix).items() if len(v) > 0}
    return len(filtered) > 0


def get_matrix_empty_spaces(matrix):
    matrix_empty_spaces = {}
    for fila in range(len(matrix)):
        empty_spaces = []
        for columna in range(len(matrix[0])):
            value = matrix[fila][columna]
            if value == " ":
                empty_spaces.append(columna)
        matrix_empty_spaces[fila] = empty_spaces

    return matrix_empty_spaces


def print_matrix(matrix, n):
    for fila in range(len(matrix)):
        print("+-" * n + "+")
        for columna in range(len(matrix[0])):
            if columna == 0:
                print("|%s" % str(matrix[fila][columna]), end="|")
            elif columna == n - 1:
                print("%s|" % str(matrix[fila][columna]))
            else:
                print(str(matrix[fila][columna]), end="|")
        if fila == n - 1:
            print("+-" * n + "+")


def change_mode():
    pass


def save():
    pass


def do_pie_operation(operation, matrix, matrix_size, game_mode):
    matrix_operations = ("S", "B", "I", "D")
    if matrix_operations.__contains__(operation):
        do_matrix_operation(matrix, operation)
        print_matrix(matrix, matrix_size)
        enter = input("Pulse cualquier tecla para mostrar inserción del nuevo bloque") == ""
        insert_new_block(matrix, game_mode)
    elif operation == "F":
        exit(0)
    elif operation == "M":
        change_mode()
    elif operation == "G":
        save()
        return None


def convert_row_to_string(matrix, row):
    return matrix[row]


def convert_column_to_string(matrix, column):
    column_word = ""
    for row in range(len(matrix)):
        column_word = column_word + matrix[row][column]
    return column_word


def do_matrix_operation(matrix, operation):
    if operation == "B":
        for column in range(len(matrix[0])):
            column_word = convert_column_to_string(matrix, column)
            gravity(column_word)
    return None


def gravity(column_word):
    return None


def random_number(origin, bound, step=1):
    """
    Obtener un número aleatorio entre el rango de [origin,bound)
    :param origin: el numero inicial inclusive
    :param bound: el numero final sin incluir
    :param step: los saltos de numero
    :return: el número aleatorio
    """
    return random.randrange(origin, bound, step)
