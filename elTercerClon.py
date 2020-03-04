# El tercer clon
import random
import os.path

nivel = range(1, 12)

print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐  CLON‐3  ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐")
print("‐ Práctica de Paradigmas de Programación 2019‐20 ‐")
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")

opciones = ("CREAR NUEVO TABLERO", "LEER TABLERO DE FICHERO", "SALIR")

# Impresión de opciones
for i in range(len(opciones)):
    print("%d. %s" % (i + 1, opciones[i]))

opcion = int(input("Indique opción : "))

#   Tamaño de la matriz
#   Debe ser cuadrada
n = 0
#   Número de obstáculos de la matriz
m = 0
#   La matriz del juego
matriz = []
#   Ruta del archivo
ruta = ""
#   Movimientos del jugador
movimientos = 0
#   Puntuacion obtenida del jugador
puntuacion = 0


def numeroaletorio(origin, bound, step=1):
    """
    Obtener un número aleatorio entre el rango de [origin,bound)
    :param origin: el numero inicial inclusive
    :param bound: el numero final sin incluir
    :param step: los saltos de numero
    :return: el número aleatorio
    """
    return random.randrange(origin, bound, step)


def imprimirtablero(matrix):
    for fila in range(len(matrix)):
        print("+-" * n + "+")
        for columna in range(len(matrix[0])):
            if columna == 0:
                print("|%s" % str(matriz[fila][columna]), end="|")
            elif columna == n - 1:
                print("%s|" % str(matriz[fila][columna]))
            else:
                print(str(matriz[fila][columna]), end="|")
        if fila == n - 1:
            print("+-" * n + "+")

    print("MOVIMIENTOS = %s |   PUNTUACIÓN = %s" % (str(movimientos), str(puntuacion)))
    return None


def crearobstaculos(m):
    obstaculos = 0
    while True:
        aleatoriofila = numeroaletorio(0, n)
        aleatoriocolumna = numeroaletorio(0, n)
        elemento = matriz[aleatoriofila][aleatoriocolumna]
        if elemento != "*":
            matriz[aleatoriofila][aleatoriocolumna] = "*"
            obstaculos += 1
        if obstaculos == m:
            break


def obstaculosdespuejugada():
    probabilidad = []
    probabilidad[1] = 0.75
    probabilidad[2] = 0.25
    return None


# Contenido del archivo leido
contenido = ""
if opcion == 1:
    n = int(input("Introduzca el tamaño de la matríz: "))
    m = int(input("Introduzca el número de obstáculos: "))
    # Creamos el tablero del juego
    matriz = [[" "] * n for i in range(n)]
    # Creación de obstaculos
    crearobstaculos(m)
    # Imprimimos el tablero
    imprimirtablero(matriz)
elif opcion == 2:
    while True:
        ruta = input("Dame la ruta del archivo")
        if os.path.isfile(ruta):
            break
    fichero = open(ruta, "r")
    contenido = fichero.read()
    fichero.flush()
    fichero.close()
elif opcion == 3:
    exit()

movimientos = {
    "S": "Subir",
    "B": "Bjar",
    "I": "zda",
    "D": "cha"
}


def pedirdatos():
    return None
