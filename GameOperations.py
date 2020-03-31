import random
import math
import os.path
from GameConfig import GameModes, GameMovements


def create_random_obstacles(matrix, n):
    """
    Creación de nuevos obstáculos aleatorios
    :param matrix: la matriz del juego
    :param n: el número de obstaculos, tiene que ser mayor o igual que 0
    :return: None si n == 0. En otro caso la propia función con n-1
    """
    # Salimos de la función si n ==0
    if n == 0:
        return None
    # Obtenemos una posición aleatoria formato : (fila, columna)
    empty_position = random_empty_space_position(matrix)
    # Escribimos el obstáculo sobre la matriz del juego
    matrix[empty_position[0]][empty_position[1]] = "*"
    # Función recursiva
    return create_random_obstacles(matrix, n - 1)


def random_empty_space_position(matrix):
    """
    Obtención de una posición aleatoria en blanco
    :param matrix: la matriz del juego
    :return: (fila, columna) posición del espacio en blanco
    """
    # Obtenemos un diccionario con el posicionamiento de los espacios en blanco
    # En formato {fila : [columnas]}
    matrix_empty_spaces = get_matrix_empty_spaces(matrix)
    # Filtramos la lista anterior usando las columnas y comprobando que haya al menos un espacio
    filtered = {k: v for k, v in matrix_empty_spaces.items() if len(v) > 0}
    # Eligimos una fila aleatoria que tenga espacios
    row, columns = random.choice(list(filtered.items()))
    # Generamos un número aleatorio
    _random_number = random_number(0, len(columns))
    # Elegimos una columna vacía aleatoria
    column = columns[_random_number]
    return row, column


def insert_new_block(matrix, game_mode):
    """
    Insertamos un nuevo bloque de nivel 1 (probabilidad de 75%) y nivel 2 (probabilidad de 25%) aleatorio
    :param matrix: la matriz del juego
    :param game_mode: el modo del juego actual
    :return: None
    """
    # Probabilidad y niveles (75% nivel 1, 25% nivel 2)
    probability = (1, 1, 1, 2)
    # Nivel elegido aleatoriamente
    level = probability[random_number(0, len(probability))]
    # Buscamos una posición del tablero de forma aleatoria
    position = random_empty_space_position(matrix)
    # Insertamos el bloque
    matrix[position[0]][position[1]] = convert_block_to_mode(str(level), GameModes.LEVEL, game_mode)
    return None


def is_possible_move(matrix):
    """
    Método que comprueba si hay al menos un espacio en blanco en el tablero del juego
    :param matrix: la matriz del juego (Tablero)
    :return: True si hay espacio/s en blanco, False si no.
    """
    # Filtramos la lista de columnas y comprobamos que haya al menos un espacio
    filtered = {k: v for k, v in get_matrix_empty_spaces(matrix).items() if len(v) > 0}
    return len(filtered) > 0


def get_matrix_empty_spaces(matrix):
    """
    Obtiene un diccionario de formato {fila : [columna]} de espacios en blanco del tablero
    :param matrix: la matriz del juego (Tablero)
    :return: el diccionario con los espacios
    """
    # Creamos un diccionario
    matrix_empty_spaces = {}
    # Bucle que recorre por filas
    for fila in range(len(matrix)):
        # Creamos una lista con las posiciones espacios en blanco
        empty_spaces = []
        # Bucle que recorre por columnas
        for columna in range(len(matrix[0])):
            # Valor del tablero
            value = matrix[fila][columna]
            # Comprobamos que sea espacio
            if value == " ":
                # Añadimos la columna a la lista
                empty_spaces.append(columna)
        # Escribimos en el diccionario
        matrix_empty_spaces[fila] = empty_spaces
    return matrix_empty_spaces


def print_matrix(game_config):
    """
    Imprimimos la matriz del juego (Tablero)
    Observaciones : la matriz tiene que ser cuadrada
    :param game_config: la configuración actual del juego
    :return: None
    """
    # Obtenemos la matriz
    matrix = game_config.get_matrix()
    # Obtenemos el tamaño de la matriz
    matrix_size = game_config.get_matrix_size()
    # Obtenemos el modo actual del juego
    current_mode = game_config.get_mode()
    # Número de guiones
    hypens = 1
    if current_mode == GameModes.LEVEL:
        hypens = 2
    elif current_mode in [GameModes.A, GameModes.B]:
        hypens = 4
    # Bucle que recorre por filas
    for fila in range(len(matrix)):
        # Imprimimos la linea de separación
        print(("+" + "-" * hypens) * matrix_size + "+")
        # Bucle que recorre por columnas
        for columna in range(len(matrix[0])):
            # Obtenemos el valor de la matriz
            value = matrix[fila][columna]
            # Comprobamos que sea un obstaculo
            if value == "*":
                # Incrementamos los obstaculos acorde con el modo del juego
                value = "*" * hypens
            # Calculamos los espacios restantes
            spaces = hypens - len(value)
            # Primera columna
            if columna == 0:
                # Imprimimos comenzando por |
                print("|" + spaces * " " + "%s" % value, end="|")
            elif columna == matrix_size - 1:  # Ultima columna
                # Imprimimos al final con |
                print(spaces * " " + "%s|" % value)
            else:  # Columnas del medio
                print(spaces * " " + value, end="|")
        # Imprimimos la última linea de separación
        if fila == matrix_size - 1:
            print(("+" + "-" * hypens) * matrix_size + "+")
    return None


def convert_block_to_mode(block, current_mode, new_mode):
    """
    Convierte la letra de un bloque de un modo a otro modo
    Observaciones: la letra debe ser la correcta del modo actual
    :param block: el bloque
    :param current_mode: el modo al que le corresponde el bloque
    :param new_mode: el nuevo modo
    :return: la letra del bloque en el nuevo modo
    """
    # Nuevo modo = Modo alfabético
    if new_mode == GameModes.ALPHA:
        # Modo actual = Modo nivel
        if current_mode == GameModes.LEVEL:
            # Resultado del caracter obtenido por ASCII de (@ + letra del bloque)
            return chr(ord("@") + int(block))
        elif current_mode == GameModes.A:  # Modo actual = Modo 1024
            # Resultado del caracter obtenido convirtiendo primero el bloque al modo nivel, y despues a modo alfabético
            return convert_block_to_mode(convert_block_to_mode(block, GameModes.A, GameModes.LEVEL), GameModes.LEVEL,
                                         GameModes.ALPHA)
        elif current_mode == GameModes.B:  # Modo actual = Modo 2048
            # Resultado del caracter obtenido convirtiendo primero el bloque al modo nivel, y despues a modo alfabético
            return convert_block_to_mode(convert_block_to_mode(block, GameModes.B, GameModes.LEVEL), GameModes.LEVEL,
                                         GameModes.ALPHA)
    elif new_mode == GameModes.LEVEL:  # Nuevo modo = Modo nivel
        if current_mode == GameModes.ALPHA:  # Modo actual = Modo alfabético
            # Resultado del caracter obtenido por ASCII del (bloque - "@")
            return str(ord(block) - ord("@"))
        elif current_mode == GameModes.A:  # Modo actual = Modo 1024
            # Resultado del caracter obtenido por ln(bloque)/ln(2) + 1
            return str(int((natural_logarithm(int(block)) / natural_logarithm(2)) + 1))
        elif current_mode == GameModes.B:  # Modo actual = Modo 2048
            # Resultado del caracter obtenido por ln(bloque)/ln(2)
            return str(int(natural_logarithm(int(block)) / natural_logarithm(2)))
    elif new_mode == GameModes.A:  # Nuevo modo = Modo 1024
        if current_mode == GameModes.ALPHA:  # Modo actual = Modo alfabético
            # Resultado del caracter obtenido por 2^nivel del bloque - 1
            return str(2 ** (ord(block) - ord("@") - 1))
        elif current_mode == GameModes.LEVEL:  # Modo actual = Modo nivel
            # Resultado del caracter obtenido por 2^nivel del bloque - 1
            return str(2 ** (int(block) - 1))
        elif current_mode == GameModes.B:  # Modo actual = Modo 2048
            # Resultado del caracter obtenido por nivel del bloque /2
            return str(int(2 / int(block)))
    elif new_mode == GameModes.B:  # Nuevo modo = Modo 2048
        if current_mode == GameModes.ALPHA:  # Modo actual = Modo alfabético
            # Resultado del caracter obtenido por 2^resultado convirtiendo el bloque al modo nivel
            return str(2 ** int(convert_block_to_mode(block, GameModes.ALPHA, GameModes.LEVEL)))
        elif current_mode == GameModes.LEVEL:  # Modo actuaL = Modo nivel
            # Resultado del caracter obtenido por 2^nivel del bloque
            return str(2 ** int(block))
        elif current_mode == GameModes.A:  # Modo actuaL = Modo 1024
            # Resultado del caracter obtenido por 2*nivel del bloque
            return str(2 * int(block))
    return block


def change_mode(game_config):
    """
    Cambio de modo del juego
    :param game_config: la configuración del juego
    :return: None
    """
    modes = ("Alfabeto", "Nivel", "1024", "2048")
    # Impresión de los modos
    for i in range(len(modes)):
        print("%d. %s" % (i + 1, modes[i]))
    # Opción elegida
    option = int(input("Escoja opción : "))
    # Modo actual
    current_mode = game_config.get_mode()
    # Nuevo modo
    new_mode = current_mode
    if option == 1:
        new_mode = GameModes.ALPHA
    elif option == 2:
        new_mode = GameModes.LEVEL
    elif option == 3:
        new_mode = GameModes.A
    elif option == 4:
        new_mode = GameModes.B
    # Comprobamos que haya elegido un modo diferente
    if current_mode != new_mode:
        # Obtenemos la matriz del juego
        matrix = game_config.get_matrix()
        # Cambiamos de modo
        game_config.set_mode(new_mode)
        # Bucle que cambia la matriz de modo
        for row in range(len(matrix)):
            for column in range(len(matrix[0])):
                value = matrix[row][column]
                # Comprobamos que no sea ni espacio ni obstaculo
                if value not in ["*", " "]:
                    new_value = convert_block_to_mode(value, current_mode, new_mode)
                    matrix[row][column] = new_value
    return None


def save(game_config):
    """
    Guardado de la partida
    :param game_config: la configuración del juego
    :return: None
    """
    # Definimos variables temporales para utilizarlas posteriormente
    matrix = game_config.get_matrix()
    current_mode = game_config.get_mode()
    # Pregunta por pantalla la ruta de guardado
    path = str(input("Indique la ruta de guardado: "))
    # Si existe archivo le eliminamos
    if os.path.isfile(path):
        os.remove(path)
    file = open(path, "a")
    # Escribir el número de movimientos y la puntuacion
    file.writelines([str(game_config.get_moves()), "\n", str(game_config.get_record())])
    # Iteracion por filas cambiando el modo de la matriz y escritura en el fichero
    for row in range(len(matrix)):
        file.write("\n")
        for column in range(len(matrix[0])):
            value = matrix[row][column]
            if value not in ["*", " "]:
                value = convert_block_to_mode(value, current_mode, GameModes.ALPHA)
            # Comprobar si el bloque esta en blanco
            if value == " ":
                file.write(".")
            else:
                file.write(value)
    file.close()


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
    """
    Método que realiza las opciones del pie
    :param operation: la operación elegida
    :param game_config: la configuración del juego
    :return: None
    """
    # Movimientos
    direction_operations = ("S", "B", "I", "D")
    if direction_operations.__contains__(operation):
        # Obtenemos los enums correspondientes
        game_operation = transform_operation(operation)
        # Matriz del juego
        matrix = game_config.get_matrix()
        # Realizamos los movimientos
        do_matrix_operation(game_operation, game_config)
        # Imprimimos la matriz
        print_matrix(game_config)
        input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")
        # Insertamos un nuevo bloque
        insert_new_block(matrix, game_config.get_mode())
        # Incrementamos una unidad el número de movimientos
        game_config.set_moves(game_config.get_moves() + 1)
    elif operation == "F":  # Salimos
        exit(0)
    elif operation == "M":  # Cambiamos de modo
        change_mode(game_config)
    elif operation == "G":  # Guardamos
        save(game_config)
    elif operation == "Z":  # Insertamos bloques
        input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")
        insert_new_block(game_config.get_matrix(), game_config.get_mode())
        return None


def convert_row_to_list(matrix, row):
    """
    Convierte una determinada fila de la matriz a una lista
    :param matrix: la matriz del juego
    :param row: el indice de la fila
    :return: el contenido de la fila en una lista
    """
    return matrix[row]


def convert_column_to_list(matrix, column):
    """
    Convierte una determinada columna de la matriz a una lista
    :param matrix: la matriz del juego
    :param column: el indice de la columna
    :return: el contenido de la columna en una lista
    """
    column_word = []
    for row in range(len(matrix)):
        column_word.append(matrix[row][column])
    return column_word


def do_matrix_operation(operation, game_config):
    """
    Realiza la acción del movimiento
    :param operation: el movimiento
    :param game_config:la configuración del juego
    :return: None
    """
    # La matriz (tablero)
    matrix = game_config.get_matrix()
    # Operaciones de bajada y subida
    if operation in [GameMovements.DOWN, GameMovements.UP]:
        for i in range(len(matrix[0])):
            # Lista de la columna convertida
            column_word_list = convert_column_to_list(matrix, i)
            # Lista de la columna después del fusionamiento
            column_word_list = get_merged_word(column_word_list, game_config, operation)
            # Insertamos la lista en la matriz
            insert_column_word(matrix, column_word_list, i)
    elif operation in [GameMovements.LEFT,
                       GameMovements.RIGHT]:  # Operaciones de mover hacia la izquierda y hacia la derecha
        for i in range(len(matrix)):
            # Lista de la fila convertida
            row_word_list = convert_row_to_list(matrix, i)
            # Lista de la fila después del fusionamiento
            row_word_list = get_merged_word(row_word_list, game_config, operation)
            # Insertamos la lista en la matriz
            insert_row_word(matrix, row_word_list, i)
    return None


def insert_row_word(matrix, words, index):
    """
    Inserta la fila en la matriz
    :param matrix: la matriz
    :param words: la lista, tiene que ser de la misma longitud que la de la matriz
    :param index: el indice de la fila
    :return: None
    """
    matrix[index] = words
    return None


def insert_column_word(matrix, words, index):
    """
    Insertamos la columna en la matriz
    :param matrix: la matriz
    :param words: la lista, tiene que ser de la misma longitud que la de la matriz
    :param index: el indice de la columna
    :return: None
    """
    for row in range(len(matrix)):
        matrix[row][index] = words[row]
    return None


def get_merged_word(_list, game_config, operation):
    """
    Fusionamiento de la lista
    :param _list: la lista de columna o de fila de la matriz
    :param game_config: la configuración del juego
    :param operation: el movimiento del juego
    :return: la lista después del fusionamiento
    """
    # Copia de la lista
    words = _list[:]
    # Obtenemos la posicíón de los obstáculos en la lista
    obstacles_positions = ([pos for pos, char in enumerate(words) if char == "*"])
    # Número de particiones, siempre será uno más que la longitud de la lista de obstaculos
    partitions = len(obstacles_positions) + 1
    # Lista de particiones
    segments = []
    # Número de espacios
    indice = 0
    # Bucle que particiona la lista de la fila o columna
    for i in range(partitions):
        # Comprobamos que es menor que la longitud
        if i < len(obstacles_positions):
            value = obstacles_positions[i]
            # Particionamos la lista de la matriz desde [indice, value]
            segments.append(words[indice:value])
            # Incrementamos el indice
            indice = value + 1
        else:
            # Particionamos la lista de la matriz desde [indice,final]
            segments.append(words[indice:])
    # Lista de la matriz reeplazada en formato (número de espacios, lista de contenido sin espacios)
    replaced = list(map(lambda y: [y.count(" "), ([char for char in y if char != " "])], segments))
    # Booleano que determina la inversibilidad
    reverse = False
    # Comprobamso que el movimiento sea hacia abajo y derecha
    if operation in [GameMovements.DOWN, GameMovements.RIGHT]:
        # Damos la vuelta a la lista
        replaced = list(map(lambda y: [y[0], y[1][::-1]], replaced))
        # Necesitamos inversar
        reverse = True
    # Bucle que hace la fusión
    for i in range(len(replaced)):
        # Segmento particionado(lista)
        segment = replaced[i][1]
        # Longitud del segmento
        segment_len = len(segment)
        # Si tiene más de una letra comprobamos que se puede hacer el fusionamiento
        if segment_len > 1:
            # Segmento fusionado(lista)
            segment_merged = merge(segment, game_config, reverse)
            # Longitud del segmento fusionado
            segment_merged_len = len(segment_merged)
            # Espacios que añadir
            spaces = segment_len - segment_merged_len
            if not spaces == 0:  # Si la diferencia no es 0 entonces incrementamos el número de espacios
                # Incrementamos el numero de espacios
                replaced[i][0] = spaces + replaced[i][0]
            # Cambiamos el valor por el segmento fusionado
            replaced[i][1] = segment_merged

    if reverse:
        for indice, value in replaced:
            for i in range(indice):
                # Insertamos los espacios en blanco en el comienzo de la lista
                value.insert(0, " ")
    else:
        for indice, value in replaced:
            for i in range(indice):
                # Insertamos los espacios en blanco en el fin de la lista
                value.append(" ")
    # Lista final de la matriz
    final_list = []
    for value in replaced:
        # Comprobamos que la longitud del segmento sea mayor que 0
        if len(value[1]) > 0:
            # Añadimos a la lista final
            final_list += value[1]
    # Insertamos los obstáculos en su determinada posición
    for value in obstacles_positions:
        final_list.insert(value, "*")

    return final_list


def merge(words, game_config, reverse=False):
    """
    Fusionamiento de bloques, por segmentos
    :param words: segmento (lista) particionada previamente
    :param game_config: configuración del juego
    :param reverse: booleano sobre la inversibilidad
    :return: segmento fusionado
    """
    # Modo actual del juego
    current_mode = game_config.get_mode()
    # Última posición del segmento que ha sufrido fusionamiento
    last_merged_index = -1
    # La letra(bloque) anterior
    last_word = ""
    # El índice del segmento(lista)
    index = 0
    # Bucle que realiza el fusionamiento
    while True:
        # Valor del segmento en una posición
        value = words[index]
        # Comprobamos que el bloque anterior coincide con el actual
        if last_word == value:
            # Indice anterior
            index_before = index - 1
            # Comprobamos que el índice anterior no sea la misma que el último guardado
            if last_merged_index != index_before:
                # Eliminamos el bloque anterior repetido
                words.pop(index_before)
                # Decrementamos el indice en una unidad
                index -= 1
                # Comprobamos que estamos en modo alfabético
                if current_mode == GameModes.ALPHA:
                    # Obtenemos el ASCII del valor siguiente
                    next_value_ascii = ord(value) + 1
                    # Obtenemos el carácter del valor siguiente
                    next_char = chr(next_value_ascii)
                    # Obtenemos el nivel del bloque fusionado
                    level = next_value_ascii - ord('@')
                else:  # Comprobamos que estamos en otros modos
                    # Obtenemos el bloque en modo nivel
                    level = int(convert_block_to_mode(value, current_mode, GameModes.LEVEL))
                    # Obtenemos el nivel siguiente
                    level += 1
                    # Convertimos el bloque en el de nivel siguiente
                    next_char = convert_block_to_mode(str(level), GameModes.LEVEL, current_mode)
                # Incrementams la puntuación acorde con el nivel del bloque fusionado
                game_config.set_record(game_config.get_record() + level)
                # Actualizamos la lista con el nuevo bloque
                words[index] = next_char
                # Actualizamos la última posición del bloque fusionado
                last_merged_index = index
                # Actualizamos la variable temporal
                value = next_char
        # Actualizamos el último bloque guardado
        last_word = value
        # Incrementamos el índice
        index += 1
        # Salimos del bucle
        if index == len(words):
            break
    if reverse:
        return words[::-1]  # Damos la vuelta a la lista
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


def natural_logarithm(x):
    """
    Calcula el logaritmo neperiano de x
    :param x: el numero deseado a calcular
    :return: el logaritmo neperiano de x
    """
    return math.log(x, math.e)
