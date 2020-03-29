# El tercer clon
# Se han considerado los estándares de nombre del Python en la realización de esta práctica :
# https://www.python.org/dev/peps/pep-0008/


from GameConfig import GameConfig
from GameOperations import print_matrix, create_random_obstacles, is_possible_move, do_pie_operation

# Impresión de la cabecera
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐  CLON‐3  ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐")
print("‐ Práctica de Paradigmas de Programación 2019‐20 ‐")
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")

# Configuración del juego
game_config = GameConfig()


# Funciones del menu principal
def new_matrix():
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
    while is_possible_move(matrix):
        # Imprimimos la matriz
        print_matrix(matrix, game_config.get_matrix_size())
        # Imprimimos el pie
        print("MOVIMIENTOS = %s |   PUNTUACIÓN = %s" % (str(game_config.get_moves()), str(game_config.get_record())))
        pie_selected_option = ""
        # Pedimos la opción del pie elegida por el jugador
        while pie_selected_option == "":
            pie_selected_option = input("[S]ubir, [B]ajar, [I]zda, [D]cha | [M]odo, [G]uardar, [F]in: ")
            # Realizamos la operacion seleccionada por el jugador
            do_pie_operation(pie_selected_option.upper(), matrix, matrix_size, game_config.get_mode())
    print("HAS PERDIDO")
    return None


def read_file():
    pass


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