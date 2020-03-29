import random

from functools import reduce

from GameConfig import GameModes, GameMovements


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
    # print("row : " + str(row) + " column : " + str(column))
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
    return None


def change_mode():
    pass


def save():
    pass


def transform_operation(word):
    operation_dict = {
        "S": GameMovements.UP,
        "B": GameMovements.DOWN,
        "I": GameMovements.LEFT,
        "D": GameMovements.RIGHT
    }
    return operation_dict[word]


def do_pie_operation(operation, matrix, matrix_size, game_mode):
    direction_operations = ("S", "B", "I", "D")
    if direction_operations.__contains__(operation):
        game_operation = transform_operation(operation)
        do_matrix_operation(matrix, game_operation)
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
    return "".join(matrix[row])


def convert_column_to_string(matrix, column):
    column_word = ""
    for row in range(len(matrix)):
        column_word = column_word + matrix[row][column]
    return column_word


def do_matrix_operation(matrix, operation):
    if operation in [GameMovements.DOWN, GameMovements.UP]:
        for i in range(len(matrix[0])):
            column_word = convert_column_to_string(matrix, i)
            column_word = get_merged_word(column_word, operation)
            insert_column_word(matrix, column_word, i)
    elif operation in [GameMovements.LEFT, GameMovements.RIGHT]:
        for i in range(len(matrix[0])):
            row_word = convert_row_to_string(matrix, i)
            row_word = get_merged_word(row_word, operation)
            insert_row_word(matrix, row_word, i)
    return None


def insert_row_word(matrix, word, index):
    matrix[index] = list(word)
    return None


def insert_column_word(matrix, word, index):
    chars = list(word)
    for row in range(len(matrix)):
        matrix[row][index] = chars[row]
    return None


def get_merged_word(word, operation):
    # obstacles_positions = ([pos for pos, char in enumerate(columnword) if char == "*"])
    test = word.split("*")
    replaced = list(map(lambda y: (y.count(" "), y.replace(" ", "")), test))
    reversed_replaced = []
    reverse = False
    if operation in [GameMovements.DOWN, GameMovements.RIGHT]:
        # Need reverse operation
        reversed_replaced = list(map(lambda y: y[1][::-1], replaced))
        reverse = True

    elif operation in [GameMovements.UP, GameMovements.LEFT]:
        reversed_replaced = list(map(lambda y: y[1], replaced))

    for i in range(len(reversed_replaced)):
        value = reversed_replaced[i]
        if len(value) > 1:
            spaces = value.count(" ")
            value = " " * spaces + merge(value, reverse)
            reversed_replaced[i] = value

    if reverse:
        replaced = list(map(lambda y, z: " " * y[0] + " " * (len(y[1]) - len(z)) + z, replaced, reversed_replaced))
    else:
        replaced = list(map(lambda y, z: z + " " * (len(y[1]) - len(z)) + " " * y[0], replaced, reversed_replaced))
    replaced = "*".join(replaced)
    return replaced


def merge(word, reverse=False):
    chars = list(word)
    last_merged_index = -1
    last_word = ""
    index = 0
    while True:
        value = chars[index]
        if last_word == value:
            if last_merged_index != index - 1:
                chars[index - 1] = ""
                next_char = chr(ord(value) + 1)
                chars[index] = next_char
                last_merged_index = index
                value = next_char
        last_word = value
        index += 1
        if index == len(chars):
            break
    result = "".join(chars)
    if reverse:
        return result[::-1]
    return result


def random_number(origin, bound, step=1):
    """
    Obtener un número aleatorio entre el rango de [origin,bound)
    :param origin: el numero inicial inclusive
    :param bound: el numero final sin incluir
    :param step: los saltos de numero
    :return: el número aleatorio
    """
    return random.randrange(origin, bound, step)
