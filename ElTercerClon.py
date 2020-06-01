# El tercer clon
# Se han considerado los estándares de nomenclatura del Python en la realización de esta práctica :
# https://www.python.org/dev/peps/pep-0008/
# autores : Mario Ramos Diez
#           Weihua Weng
# Github link de este proyecto : https://github.com/firework0512/PP


from GameConfig import GameConfig
from GameOperations import print_matrix, create_random_obstacles, is_possible_move, do_pie_operation

# Impresión de la cabecera
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐  CLON‐3  ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐")
print("‐ Práctica de Paradigmas de Programación 2019‐20 ‐")
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")

# Configuración del juego
game_config = GameConfig()

# Pie
pie = "[S]ubir, [B]ajar, [I]zda, [D]cha | [M]odo, [G]uardar, [F]in: "


# Funciones del menu principal
def new_matrix():
    """
    Crea una nueva matriz del juego (Nueva partida)
    :return: None
    """
    # Pedimos datos
    matrix_size = int(input("Introduzca el tamaño de la matríz: "))
    game_config.set_matrix_size(matrix_size)
    obstacles = int(input("Introduzca el número de obstáculos: "))
    while obstacles > matrix_size * matrix_size:
        print("No caben tantos obstáculos en la matriz")
        obstacles = int(input("Introduzca el número de obstáculos: "))
    game_config.set_obstacles(obstacles)
    matrix = game_config.get_matrix()
    # Creamos los obstáculos
    create_random_obstacles(matrix, obstacles)
    # Comprobamos que se puede realizar el movimiento
    do_action(matrix)
    return None


def do_action(matrix, is_first_entry=True):
    """
    Método que comprueba si es posible realizar un movimiento. Si es el caso, se pide el usuario el movimiento,
    por el lado contrario se termina la partida.
    :param matrix: la matriz del juego (tablero)
    :param is_first_entry: booleano que determina la necesidad de insertar bloques al comienzo
    :return: None
    """
    while is_possible_move(matrix):
        # Imprimimos la matriz
        print_matrix(game_config)
        # Imprimimos el pie
        print("MOVIMIENTOS = %s |   PUNTUACIÓN = %s" % (str(game_config.get_moves()), str(game_config.get_record())))
        # Comprobamos si hace falta insertar bloque porque acabamos de crear la matriz
        if is_first_entry:
            do_pie_operation("Z", game_config)
            is_first_entry = False
        else:
            # Opción del pie elegida por el jugador
            pie_selected_option = ""
            # Pedimos la opción del pie al jugador
            while pie_selected_option == "":
                pie_selected_option = input(pie)
                # Realizamos la operacion seleccionada por el jugador
                do_pie_operation(pie_selected_option.upper(), game_config)
    # Imprimimos la matriz
    print_matrix(game_config)
    print("HAS PERDIDO")
    return None


def read_file(path):
    """
    Método que lee un fichero y luego empieza la partida del juego
    :return: None
    """
    # Contenido de la lectura
    txt = []
    # Inserta lineas del fichero en la lista
    with open(path) as file:
        for line in file:
            txt.append(line)
    # Actualizamos los movimientos y la puntuación almacenada en el fichero
    game_config.set_moves(int(txt[0]))
    game_config.set_record(int(txt[1]))
    # Inicio la matriz
    game_config.set_matrix_size(int(len(txt[2]) - 1))
    # Carga la matriz
    matrix = game_config.get_matrix()
    # Inserta caracteres en la matriz
    for row in range(len(txt[2]) - 1):
        line = txt[row + 2]
        for column in range(len(txt[2]) - 1):
            if not line[column] == ".":
                matrix[row][column] = line[column]
            else:
                matrix[row][column] = " "
    game_config.set_matrix(matrix)
    do_action(matrix, False)
    return None


# Opciones del menu principal
menu_options = ("CREAR NUEVO TABLERO", "LEER TABLERO DE FICHERO", "SALIR")
# Impresión de opciones
for i in range(len(menu_options)):
    print("%d. %s" % (i + 1, menu_options[i]))

# Opción del menu principal elegida por el jugador
menu_options = int(input("Indique opción : "))

if menu_options == 1:
    new_matrix()
elif menu_options == 2:
    read_file()
elif menu_options == 3:
    exit()
