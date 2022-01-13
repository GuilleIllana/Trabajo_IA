import Board_lib
import numpy as np

def expanded_board(Board): #cutre, cutre
    m = []
    r = []
    for j in range(Board.cols + 2):
        r.append(20) # borde
    m.append(r)

    for i in range(Board.rows):
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
        return na, oa[-1] # carry-out = 1 if oa[end] was 1

def check_value(ec_sys, value):
    s = []
    for j in range(len(ec_sys[0])):
        for i in range(len(ec_sys)):
            if ec_sys[i][j] != value:
                break
            elif i == len(ec_sys) - 1:
                s.append(j)
    return s

def uncompress_1(n, row, col):
    k = 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            elif n == k:
                return row+i, col+j
            k = k + 1
    return -1


def solve_system_1(eb, row, col):
    n1 = eb[row+1][col+1]
    candidate_simp_sys = []
    inc = []

    k = 0
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            elif eb[row+i][col+j] == 9: #unknown
                inc.append(k) # se añade a la lista de incógnitas
                candidate_simp_sys.append(False)
            elif eb[row+i][col+j] == 10: #flag
                n1 = n1 - 1 # se le resta 1 al valor de la suma
            k = k+1

    if len(inc) == 0:
        return -1, -1, -1 #no hay ninguna incógnita alrededor


    valid_simp_sys = []
    # todas las posibilidades
    for i in range(2**len(inc)):
        candidate_simp_sys, basura = new_possible_solution(candidate_simp_sys)
        if sum(candidate_simp_sys) == n1:
            valid_simp_sys.append(candidate_simp_sys)

    if len(valid_simp_sys) == 0:
        return -1, -1, -1
    v = check_value(valid_simp_sys, 1) #1 = mina -> POSIBLE CAMBIO DE ORDEN MAAAAN
    if len(v) != 0:
        rm, cm = uncompress_1(inc[v[0]], row, col)
        #eb[rm][cm] = 10
        return rm, cm, 1

    v = check_value(valid_simp_sys, 0)  # 0 = no mina -> pulsar
    if len(v) != 0:
        rn, cn = uncompress_1(inc[v[0]], row, col)
        #eb[rn][cn] = 15 ## prueba
        return rn, cn, 0
    else:
        return -1, -1, -1





