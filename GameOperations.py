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


def save(game_config):
    matrix = game_config.get_matrix()
    path = str (input ("Indique la ruta de guardado: "))
    file = open (path, "a")
    file.writelines([str(game_config.get_moves()), "\n", str(game_config.get_record())])
    for row in range(len(matrix)):
        file.write("\n")
        for column in range(len(matrix[0])):
            if matrix[row][column] == " ":
                file.write(".")
            else:
                file.write(matrix[row][column])
            column += 1
        row += 1



def transform_operation(word):
    """
    Cambia la letra del movimiento por los enums definidos de las operaciones
    Observaciones : la letra tiene que ser uno de estos "S", "B", "I", "D"
    :param word: la letra de la operación
    :return: los movimientos del juego definidos dentro de GameMovements
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
        save(game_config)
    elif operation == "Z":
        input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")
        insert_new_block(game_config.get_matrix(), game_config.get_mode())
        return None


def convert_row_to_string(matrix, row):
    return "".join(matrix[row])


def convert_column_to_string(matrix, column):
    column_word = ""
    for row in range(len(matrix)):
        column_word = column_word + matrix[row][column]
    return column_word


def do_matrix_operation(operation, game_config):
    matrix = game_config.get_matrix()
    if operation in [GameMovements.DOWN, GameMovements.UP]:
        for i in range(len(matrix[0])):
            column_word = convert_column_to_string(matrix, i)
            column_word = get_merged_word(column_word, operation, game_config)
            insert_column_word(matrix, column_word, i)
    elif operation in [GameMovements.LEFT, GameMovements.RIGHT]:
        for i in range(len(matrix)):
            row_word = convert_row_to_string(matrix, i)
            row_word = get_merged_word(row_word, operation, game_config)
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


def get_merged_word(word, operation, game_config):
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
            value = " " * spaces + merge(value, game_config, reverse)
            reversed_replaced[i] = value

    if reverse:
        replaced = list(map(lambda y, z: " " * y[0] + " " * (len(y[1]) - len(z)) + z, replaced, reversed_replaced))
    else:
        replaced = list(map(lambda y, z: z + " " * (len(y[1]) - len(z)) + " " * y[0], replaced, reversed_replaced))
    replaced = "*".join(replaced)
    return replaced


def merge(word, game_config, reverse=False):
    chars = list(word)
    current_mode = game_config.get_mode()
    last_merged_index = -1
    last_word = ""
    index = 0
    while True:
        value = chars[index]
        if last_word == value:
            if last_merged_index != index - 1:
                chars[index - 1] = ""
                if current_mode == GameModes.ALPHA:
                    next_value_ascii = ord(value) + 1
                    next_char = chr(next_value_ascii)
                    level = next_value_ascii - ord('@')
                else:
                    level = int(convert_block_to_mode(value, current_mode, GameModes.LEVEL))
                    level += 1
                    next_char = convert_block_to_mode(str(level), GameModes.LEVEL, current_mode)
                game_config.set_record(game_config.get_record() + level)
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
