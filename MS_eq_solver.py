import Board_lib
import numpy as np

# Minesweeper equation system solver via model checking

def expanded_board(Board):
    # para ponerle un "borde" al tablero (se amplían las dimensiones). Es cutre, lo sé :)
    m = []
    r = []
    for j in range(Board.cols + 2):
        r.append(20) # borde
    m.append(r)

    for i in range(Board.rows): # copia el tablero board, básicamente
        r = [20]
        for j in range(Board.cols):
            r.append(Board.cell[i][j].state)
        r.append(20)
        m.append(r)

    r = []
    for j in range(Board.cols + 2):
        r.append(20) # borde
    m.append(r)

    return m

def new_possible_solution(oa):
    # a partir de un vector binario de 0/False (no mina) y 1/True (mina((False y True), donde este vector simboliza un
    # posible modelo del mundo (model checking), se genera otro vector. Funciona básicamente como un sumador binario en 
    # cadena
    if len(oa) > 1:
        na, c = new_possible_solution(oa[:-1])
    else:
        c = True
        na = []
    if not c: # not carry out - not change
        na.append(oa[-1])
        return na, False
    else: # change
        na.append(not oa[-1])
        return na, oa[-1] # carry out = 1 if oa[end] was 1

def check_value(ec_sys, value):
    # comprueba si el valor value se encuentra en todos los vectores de soluciones válidos, y devuelve la posición de estos
    s = []
    for j in range(len(ec_sys[0])):
        for i in range(len(ec_sys)):
            if ec_sys[i][j] != value:
                break
            elif i == len(ec_sys) - 1:
                s.append(j)
    return s

# --- 1 ECUACIÓN ---

def get_coords_1(n, row, col):
    # transforma una solución en las coordenadas del tablero (1 ecuación)
    k = 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            elif n == k:
                return row+i, col+j
            k += 1
    return -1

def solve_system_1(eb, row, col):
    # resuelve el sistema de ecuaciones (en realidad, solo una ecuación) de una casilla
    n1 = eb[row + 1][col + 1] #  (término independiente de la ecuación 1) # valor de la casilla central (término independiente de la ecuación)
    candidate_solutions = [] # soluciones candidatas
    inc = [] # incógnitas (vector que representa las posiciones de las casillas colindadntes sin descubrir)

    k = 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            elif eb[row+i][col+j] == 9: # unknown, not discovered
                inc.append(k) # se añade a la lista de incógnitas
                candidate_solutions.append(False) # el vector de soluciones candidatas empieza inicializado en ceros
            elif eb[row+i][col+j] == 10: # flag
                n1 = n1 - 1 # se le resta 1 al valor de la suma
            k += 1

    if len(inc) == 0:
        return -1, -1, -1  # no hay ninguna incógnita alrededor

    valid_solutions = []
    # todas las posibilidades
    for i in range(2**len(inc)):
        candidate_solutions, basura = new_possible_solution(candidate_solutions)
        if sum(candidate_solutions) == n1:
            valid_solutions.append(candidate_solutions)

    if len(valid_solutions) == 0: # no hay un solo valor del sistema que cumpla las ecuaciones
        # (lo cual no sé muy bien por qué ocurre)
        return -1, -1, -1

    v = check_value(valid_solutions, 0)  # 0 = no mina -> pulsar
    if len(v) != 0:
        rn, cn = get_coords_1(inc[v[0]], row, col)
        return rn, cn, 0 # row, column, not mine

    v = check_value(valid_solutions, 1) # 1 = mina -> banderita
    if len(v) != 0:
        rm, cm = get_coords_1(inc[v[0]], row, col)
        return rm, cm, 1 # row, column, mine
    else:
        return -1, -1, -1

# --- 2 ECUACIONES VERTICAL ---

def get_coords_2v(n, row, col):
    # transforma una solución en las coordenadas del tablero (2 ecuaciones, vertical)
    k = 0
    for i in range(4):
        for j in range(3):
            if (i == 1 or i == 2) and j == 1:
                continue
            elif n == k:
                return row + i, col + j
            k += 1
    return -1

def solve_system_2v(eb, row, col):
    # resuelve el sistema de ecuaciones de dos casillas consecutivas en vertical
    n1 = eb[row + 1][col + 1] # (término independiente de la ecuación 1)
    n2 = eb[row + 2][col + 1] # (término independiente de la ecuación 2)
    candidate_solutions = [] # soluciones candidatas
    inc = [] # incógnitas (vector que representa las posiciones de las casillas colindadntes sin descubrir)

    # ec. 1 -> filas (i) 0 a 2
    # ec. 2 -> filas (i) 1 a 3
    k = 0
    for i in range(4):
        for j in range(3):
            if (i == 1 or i == 2) and j == 1:
                continue
            elif i == 1 and j == 0:
                start2 = len(inc) # marca que indica desde qué parte del vector se corresponde con la ecuación 2
            elif i == 3 and j == 0:
                end1 = len(inc) # marca que indica hasta qué parte del vector se corresponde con la ecuación 1
            if eb[row+i][col+j] == 9: # unknown
                inc.append(k) # se añade a la lista de incógnitas
                candidate_solutions.append(False)
            elif eb[row+i][col+j] == 10: #flag
                if i <= 2:
                    n1 = n1 - 1 # se le resta 1 al valor de la suma (ec 1)
                if i >= 1:
                    n2 = n2 - 1 # se le resta 1 al valor de la suma (ec 2)
            k += 1

    if len(inc) == 0:
        return -1, -1, -1 # no hay ninguna incógnita alrededor

    valid_solutions = []
    # todas las posibilidades
    for i in range(2**len(inc)):
        candidate_solutions, basura = new_possible_solution(candidate_solutions)
        if sum(candidate_solutions[:end1]) == n1 and sum(candidate_solutions[start2:]) == n2:
            valid_solutions.append(candidate_solutions)

    if len(valid_solutions) == 0:
        return -1, -1, -1

    v = check_value(valid_solutions, 0) # 0 = no mina -> pulsar
    if len(v) != 0:
        rn, cn = get_coords_2v(inc[v[0]], row, col)
        return rn, cn, 0

    v = check_value(valid_solutions, 1) # 1 = mina -> banderita
    if len(v) != 0:
        rm, cm = get_coords_2v(inc[v[0]], row, col)
        return rm, cm, 1
    else:
        return -1, -1, -1

# --- 2 ECUACIONES HORIZONTAL ---

def get_coords_2h(n, row, col):
    # transforma una solución en las coordenadas del tablero (2 ecuaciones, horizontal)
    k = 0
    for j in range(4):
        for i in range(3):
            if (j == 1 or j == 2) and i == 1:
                continue
            elif n == k:
                return row + i, col + j
            k += 1
    return -1

def solve_system_2h(eb, row, col):
    # resuelve el sistema de ecuaciones de dos casillas consecutivas en horizontal
    n1 = eb[row + 1][col + 1] # (término independiente de la ecuación 1)
    n2 = eb[row + 1][col + 2] # (término independiente de la ecuación 2)
    candidate_solutions = [] # soluciones candidatas
    inc = [] # incógnitas (vector que representa las posiciones de las casillas colindadntes sin descubrir)

    # ec. 1 -> columnas (j) 0 a 2
    # ec. 2 -> columnas (j) 1 a 3
    k = 0
    for j in range(4):
        for i in range(3):
            if (j == 1 or j == 2) and i == 1:
                continue
            elif j == 1 and i == 0:
                start2 = len(inc) # marca que indica desde qué parte del vector se corresponde con la ecuación 2
            elif j == 3 and i == 0:
                end1 = len(inc) # marca que indica hasta qué parte del vector se corresponde con la ecuación 1
            if eb[row+i][col+j] == 9: # unknown
                inc.append(k) # se añade a la lista de incógnitas
                candidate_solutions.append(False)
            elif eb[row+i][col+j] == 10: # flag
                if j <= 2:
                    n1 = n1 - 1 # se le resta 1 al valor de la suma (ec 1)
                if j >= 1:
                    n2 = n2 - 1 # se le resta 1 al valor de la suma (ec 2)
            k += 1

    if len(inc) == 0: # no hay ninguna incógnita alrededor
        return -1, -1, -1

    valid_solutions = []
    # todas las posibilidades
    for i in range(2**len(inc)):
        candidate_solutions, basura = new_possible_solution(candidate_solutions)
        if sum(candidate_solutions[:end1]) == n1 and sum(candidate_solutions[start2:]) == n2:
            valid_solutions.append(candidate_solutions)

    if len(valid_solutions) == 0:
        return -1, -1, -1

    v = check_value(valid_solutions, 0) # 0 = no mina -> pulsar
    if len(v) != 0:
        rn, cn = get_coords_2h(inc[v[0]], row, col)
        return rn, cn, 0

    v = check_value(valid_solutions, 1) # 1 = mina -> banderita
    if len(v) != 0:
        rm, cm = get_coords_2h(inc[v[0]], row, col)
        return rm, cm, 1
    else:
        return -1, -1, -1

