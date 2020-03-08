# El tercer clon
import random
import os.path

mod = 1
nivel = range(1, 12)

print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐  CLON‐3  ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐")
print("‐ Práctica de Paradigmas de Programación 2019‐20 ‐")
print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")

opciones = ("CREAR NUEVO TABLERO", "LEER TABLERO DE FICHERO", "SALIR")
jugadas = ("Alfabeto", "Nivel", "1024", "2048")
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
    enter = False
    jugada=""
    # Entrada de jugadas
    while jugada == "":
        jugada=input("[S]ubir, [B]ajar, [I]zda, [D]cha | [M]odo, [G]uardar, [F]in: ")
        if(validajugada(jugada)==False):
            print("Entrada no valida")
            jugada == ""
    Jugadas(jugada)
    if input("Pulse cualquier tecla para mostrar inserción del nuevo bloque")=="":
        enter=True
    if enter:
        print("f")
    return None

# Jugadas del tablero
def subir():
    print("elegiste subir")
def bajar():
    print("elegiste bajar")
def izda():
    print("elegiste izquierda")
def dcha():
    print("elegiste derecha")
def modo():
   # return "elegiste modo"
    print("ESCOJA MODO DE VISUALIZACION: \n")
    for i in range(len(jugadas)):
        print("%d. %s" % (i + 1, jugadas[i]))
    mod = input("\n Escoja opcion: ")

def guardar():
    print("elegiste guardar")
def fin():
    print("elegiste fin")

def Jugadas(jugad):
    jugad = jugad.upper()
    funcion = " "
    opciones = {
        "S": subir,
        "B": bajar,
        "I": izda,
        "D": dcha,
        "M": modo,
        "G": guardar,
        "F": fin
    }
    funcion = opciones.get(jugad, "No existe")
    funcion()

# Validar la entrada
def validajugada(jug):
    jug=jug.upper()
    lista = ["S", "B", "I", "D", "M", "G", "F"]
    i = 0
    for i in range(len(lista)):
        if jug == lista[i]:
            return True
        i += 1
    return False

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




def pedirdatos():
    return None
