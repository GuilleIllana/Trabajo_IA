# This file tries to generate diferent random boards in order to generate a dataset to feed a neural network
import math

import numpy as np
import random

mine_number = 11


def generate_board(rows, col, n_mines):

    board = np.zeros([int(rows), int(col)])

    if n_mines > (rows*col-1):
        print('Max number of mines exceeded\n')
        return board

    # Generate diferent random mine positions
    mine_pos = random.sample(range(0, rows*col), n_mines)
    mine_pos.sort()

    print(mine_pos)
    # Place mines
    for i in mine_pos:
        print(i)
        print('i='+str(math.floor(i/col)) + ' j='+str(i-math.floor(i/col)*col))
        board[math.floor(i/col), i-math.floor(i/col)*col] = mine_number

    # Calc number of mines of each position
    for i in range(rows):
        for j in range(col):
            if board[i, j] != mine_number:
                if i != (rows-1) and i != 0 and j != (col-1) and j != 0:
                    print('1er if '+'i' + str(i) + ' j' + str(j))
                    near_mines = [i for horizontal in range(-1, 2) for vertical in range(-1, 2) if board[i+vertical, j + horizontal] == mine_number]

                    print(len(near_mines))
                    board[i, j] = len(near_mines)
                elif i == 0:
                    print('2o if'+'i' + str(i) + ' j' + str(j))
                    if j == 0:
                        near_mines = [i for horizontal in range(0, 2) for vertical in range(0, 2) if board[i + vertical, j + horizontal] == mine_number]
                    elif j == (col-1):
                        near_mines = [i for horizontal in range(-1, 1) for vertical in range(0, 2) if board[i + vertical, j + horizontal] == mine_number]
                    else:
                        near_mines = [i for horizontal in range(-1, 2) for vertical in range(0, 2) if board[i + vertical, j + horizontal] == mine_number]

                    print(len(near_mines))
                    board[i, j] = len(near_mines)
                elif j == 0:
                    print('3er if ' + 'i' + str(i) + ' j' + str(j))
                    if i == (rows - 1):
                        near_mines = [i for horizontal in range(0, 2) for vertical in range(-1, 1) if board[i + vertical, j + horizontal] == mine_number]
                    else:
                        near_mines = [i for horizontal in range(0, 2) for vertical in range(-1, 2) if board[i + vertical, j + horizontal] == mine_number]

                    print(len(near_mines))
                    board[i, j] = len(near_mines)
                elif i == (rows-1):
                    if j == (col-1):
                        near_mines = [i for horizontal in range(-1, 1) for vertical in range(-1, 1) if board[i + vertical, j + horizontal] == mine_number]
                    else:
                        near_mines = [i for horizontal in range(-1, 2) for vertical in range(-1, 1) if board[i + vertical, j + horizontal] == mine_number]

                    print(len(near_mines))
                    board[i, j] = len(near_mines)
                else:
                    near_mines = [i for horizontal in range(-1, 1) for vertical in range(-1, 2) if board[i + vertical, j + horizontal] == mine_number]

                    print(len(near_mines))
                    board[i, j] = len(near_mines)
                    continue

    return board

