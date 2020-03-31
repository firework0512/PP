import random
import math
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
    block = "A"
    if level == 2:
        block = "B"
    matrix[position[0]][position[1]] = convert_block_to_mode(block, GameModes.ALPHA, game_mode)
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


def print_matrix(game_config):
    matrix = game_config.get_matrix()
    matrix_size = game_config.get_matrix_size()
    current_mode = game_config.get_mode()
    hypens = 1
    if current_mode == GameModes.LEVEL:
        hypens = 2
    elif current_mode in [GameModes.A, GameModes.B]:
        hypens = 4

    for fila in range(len(matrix)):
        print(("+" + "-" * hypens) * matrix_size + "+")
        for columna in range(len(matrix[0])):
            value = matrix[fila][columna]
            if value == "*":
                value = "*" * hypens
            spaces = hypens - len(value)
            if columna == 0:
                print("|" + spaces * " " + "%s" % value, end="|")
            elif columna == matrix_size - 1:
                print(spaces * " " + "%s|" % value)
            else:
                print(spaces * " " + value, end="|")
        if fila == matrix_size - 1:
            print(("+" + "-" * hypens) * matrix_size + "+")
    return None


def natural_logarithm(x):
    """
    Calcula el logaritmo neperiano de x
    :param x: el numero deseado a calcular
    :return: el logaritmo neperiano de x
    """
    return math.log(x, math.e)


def convert_block_to_mode(block, current_mode, new_mode):
    """
    Convierte la letra de un bloque de un modo a otro modo
    :param block: el bloque
    :param current_mode: el modo al que le corresponde el bloque
    :param new_mode: el nuevo modo
    :return: la letra del bloque en el nuevo modo
    """
    if new_mode == GameModes.ALPHA:
        if current_mode == GameModes.LEVEL:
            return chr(ord("@") + int(block))
        elif current_mode == GameModes.A:
            return convert_block_to_mode(convert_block_to_mode(block, GameModes.A, GameModes.LEVEL), GameModes.LEVEL,
                                         GameModes.ALPHA)
        elif current_mode == GameModes.B:
            return convert_block_to_mode(convert_block_to_mode(block, GameModes.B, GameModes.LEVEL), GameModes.LEVEL,
                                         GameModes.ALPHA)
    elif new_mode == GameModes.LEVEL:
        if current_mode == GameModes.ALPHA:
            return str(ord(block) - ord("@"))
        elif current_mode == GameModes.A:
            return str(int((natural_logarithm(int(block)) / natural_logarithm(2)) + 1))
        elif current_mode == GameModes.B:
            return str(int(natural_logarithm(int(block)) / natural_logarithm(2)))
    elif new_mode == GameModes.A:
        if current_mode == GameModes.ALPHA:
            return str(2 ** (ord(block) - ord("@") - 1))
        elif current_mode == GameModes.LEVEL:
            return str(2 ** (int(block) - 1))
        elif current_mode == GameModes.B:
            return str(int(2 / int(block)))
    elif new_mode == GameModes.B:
        if current_mode == GameModes.ALPHA:
            return str(2 ** int(convert_block_to_mode(block, GameModes.ALPHA, GameModes.LEVEL)))
        elif current_mode == GameModes.LEVEL:
            return str(2 ** int(block))
        elif current_mode == GameModes.A:
            return str(2 * int(block))
    return block


def change_mode(game_config):
    """
    Cambio de modo del juego
    :param game_config: la configuración del juego
    :return: None
    """
    modes = ("Alfabeto", "Nivel", "1024", "2048")
    for i in range(len(modes)):
        print("%d. %s" % (i + 1, modes[i]))
    option = int(input("Escoja opción : "))
    current_mode = game_config.get_mode()
    new_mode = current_mode
    if option == 1:
        new_mode = GameModes.ALPHA
    elif option == 2:
        new_mode = GameModes.LEVEL
    elif option == 3:
        new_mode = GameModes.A
    elif option == 4:
        new_mode = GameModes.B
    if current_mode != new_mode:
        matrix = game_config.get_matrix()
        game_config.set_mode(new_mode)
        for row in range(len(matrix)):
            for column in range(len(matrix[0])):
                value = matrix[row][column]
                if value not in ["*", " "]:
                    new_value = convert_block_to_mode(value, current_mode, new_mode)
                    matrix[row][column] = new_value
    return None


def save():
    pass


def transform_operation(word):
    """
    Cambia la letra del movimiento por los enums definidos de las operaciones
    Observaciones : la letra tiene que ser uno de estos "S", "B", "I", "D"
    :param word: la letra de la operación
    :return: los movimientos del juego definidos dentro de la clase enum GameMovements
    """
    operation_dict = {
        "S": GameMovements.UP,
        "B": GameMovements.DOWN,
        "I": GameMovements.LEFT,
        "D": GameMovements.RIGHT
    }
    return operation_dict[word]


def do_pie_operation(operation, game_config):
    direction_operations = ("S", "B", "I", "D")

    if direction_operations.__contains__(operation):
        game_operation = transform_operation(operation)
        matrix = game_config.get_matrix()
        do_matrix_operation(game_operation, game_config)
        print_matrix(game_config)
        input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")
        insert_new_block(matrix, game_config.get_mode())
        # Incrementamos una unidad el número de movimientos
        game_config.set_moves(game_config.get_moves() + 1)
    elif operation == "F":
        exit(0)
    elif operation == "M":
        change_mode(game_config)
    elif operation == "G":
        save()
    elif operation == "Z":
        input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")
        insert_new_block(game_config.get_matrix(), game_config.get_mode())
        return None


def convert_row_to_list(matrix, row):
    """
    Convierte una determinada fila de la matriz a un string
    :param matrix: la matriz del juego
    :param row: el indice de la fila
    :return: el contenido de la fila en string
    """
    return matrix[row]


def convert_column_to_list(matrix, column):
    """
    Convierte una determinada columna de la matriz a un string
    :param matrix: la matriz del juego
    :param column: el indice de la columna
    :return: el contenido de la columna en string
    """
    column_word = []
    for row in range(len(matrix)):
        column_word.append(matrix[row][column])
    return column_word


def do_matrix_operation(operation, game_config):
    matrix = game_config.get_matrix()
    if operation in [GameMovements.DOWN, GameMovements.UP]:
        for i in range(len(matrix[0])):
            column_word_list = convert_column_to_list(matrix, i)
            # print("old column word list :", column_word_list)
            column_word_list = get_merged_word(column_word_list, game_config, operation)
            # print("column word list :", column_word_list)
            insert_column_word(matrix, column_word_list, i)
    elif operation in [GameMovements.LEFT, GameMovements.RIGHT]:
        for i in range(len(matrix)):
            row_word_list = convert_row_to_list(matrix, i)
            row_word_list = get_merged_word(row_word_list, game_config, operation)
            # print("row word list :", row_word_list)
            insert_row_word(matrix, row_word_list, i)
    return None


def insert_row_word(matrix, words, index):
    matrix[index] = words
    return None


def insert_column_word(matrix, words, index):
    for row in range(len(matrix)):
        matrix[row][index] = words[row]
    return None


def get_merged_word(words, game_config, operation):
    obstacles_positions = ([pos for pos, char in enumerate(words) if char == "*"])
    spaces = 0
    size = len(obstacles_positions) + 1
    segments = []

    for i in range(size):
        if i < len(obstacles_positions):
            value = obstacles_positions[i]
            segments.append(words[spaces:value])
            spaces = value + 1
        else:
            segments.append(words[spaces:])

    # print("segments :", segments)
    replaced = list(map(lambda y: [y.count(" "), ([char for char in y if char != " "])], segments))
    # print("replaced :", replaced)
    reverse = False
    if operation in [GameMovements.DOWN, GameMovements.RIGHT]:
        replaced = list(map(lambda y: [y[0], y[1][::-1]], replaced))
        reverse = True
    elif operation in [GameMovements.UP, GameMovements.LEFT]:
        replaced = list(map(lambda y: [y[0], y[1]], replaced))

    for i in range(len(replaced)):
        segment = replaced[i][1]
        segment_len = len(segment)
        if segment_len > 1:
            # print("segment :", segment)
            segment_merged = merge(segment, game_config, reverse)
            # print("segment merged :", segment_merged)
            segment_merged_len = len(segment_merged)
            spaces = segment_len - segment_merged_len
            if not spaces == 0:
                replaced[i][0] = spaces + replaced[i][0]
            replaced[i][1] = segment_merged

    if reverse:
        for spaces, value in replaced:
            for i in range(spaces):
                value.insert(0, " ")
    else:
        for spaces, value in replaced:
            for i in range(spaces):
                value.append(" ")
    # print("replaced final :", replaced)
    final_list = []
    for value in replaced:
        if len(value[1]) > 0:
            final_list += value[1]
    # return list(map(lambda y: add_empty_spaces(y[1]), replaced))
    for value in obstacles_positions:
        final_list.insert(value, "*")
    return final_list


def add_empty_spaces(list):
    if len(list) > 0:
        return list
    else:
        return ["*"]


def merge(words, game_config, reverse=False):
    current_mode = game_config.get_mode()
    last_merged_index = -1
    last_word = ""
    index = 0
    while True:
        value = words[index]
        if last_word == value:
            index_before = index - 1
            if last_merged_index != index_before:
                words.pop(index_before)
                index -= 1
                if current_mode == GameModes.ALPHA:
                    next_value_ascii = ord(value) + 1
                    next_char = chr(next_value_ascii)
                    level = next_value_ascii - ord('@')
                else:
                    level = int(convert_block_to_mode(value, current_mode, GameModes.LEVEL))
                    level += 1
                    next_char = convert_block_to_mode(str(level), GameModes.LEVEL, current_mode)
                game_config.set_record(game_config.get_record() + level)
                words[index] = next_char
                last_merged_index = index
                value = next_char
        last_word = value
        index += 1
        if index == len(words):
            break
    if reverse:
        return words[::-1]
    return words


def random_number(origin, bound, step=1):
    """
    Obtiene un número aleatorio entre el rango de [origin,bound)
    :param origin: el numero inicial inclusive
    :param bound: el numero final sin incluir
    :param step: los saltos de numero
    :return: el número aleatorio
    """
    return random.randrange(origin, bound, step)
