import numpy as np
import copy
import WinCaptureFunctions as wcf
from Cell_lib import Cell


class Board:
    def __init__(self, rows, columns, solved=False, dead=False):
        self.rows = rows
        self.cols = columns
        self.solved = solved
        self.dead = dead
        # If we don't use deep copy all the Cell objects are the same so they doesn't update properly
        #Order of creation mathers..
        col_list = [Cell(False, 9, 88) for i in range(self.cols)]
        self.cell = [copy.deepcopy(col_list) for j in range(self.rows)]
        # Obtaining the initial state of the board
        self.template = wcf.init_template()
        self.update_board()

    def new_game(self):
        # Clicking the board to start new game
        wcf.click_board(int(self.cols / 2), -2)
        self.update_board()
        self.solved = False
        self.dead = False

    def check_dead(self):
        # Change number to 13 cause a clicked bomb is 13 state
        idx = np.argwhere(self.obtain_matrix() == 13)
        dead = True if idx.shape[0] != 0 else False
        return dead

    def check_solved(self):
        idx = np.argwhere(self.obtain_matrix() == 9)
        solved = True if idx.shape[0] == 0 else False
        return solved

    def update_board(self):
        # Obtaining the matrix that reflects the state of the game
        board_image = wcf.loadBoard('buscaminas')
        mat = wcf.obtainMatrix(board_image, self.template)
        while np.isnan(mat).any():
            mat = wcf.obtainMatrix(board_image, self.template)

        # update contains the coordinates which has changed in this iteration
        update = np.argwhere(self.obtain_matrix() - mat)
        for idx in update:
            # This loop updates every cell state which has changed
            row, col = idx[0], idx[1]
            self.cell[row][col].update_state(int(mat[row][col]))

        """for i in range(self.rows):
            for j in range(self.cols):
                self.cell[i][j].update_state(int(mat[i][j]))"""

        # Updating the dead state
        self.dead = self.check_dead()

        # Updating discovered state
        self.calc_discovered()

        # Updating undiscovered neighbours
        self.calc_undiscovered_neighbours()

        # Updating heuristics
        self.calc_heuristic()

    def obtain_matrix(self):
        # This function returns a matrix representing the cells states
        matrix = np.zeros((self.rows, self.cols), dtype=int)
        for i in range(self.rows):
            for j in range(self.cols):
                matrix[i][j] = self.cell[i][j].state
        return matrix

    def show_board(self):
        print("State of the board")
        for i in range(self.rows):
            print('[', end='\t')
            for j in range(self.cols):
                print(self.cell[i][j].state, end='\t')
            print(']')
        print(end="\n\n")

    def show_discovered(self):
        print("Discovered state")
        for i in range(self.rows):
            print('[', end='\t')
            for j in range(self.cols):
                if self.cell[i][j].discovered:
                    print("1", end='\t')
                else:
                    print("0", end='\t')
            print(']')
        print(end="\n\n")

    def show_undiscovered_neighbours(self):
        print("Undiscovered neighbours")
        for i in range(self.rows):
            print('[', end='\t')
            for j in range(self.cols):
                print(self.cell[i][j].undiscovered_neighbours, end='\t')
            print(']')
        print(end="\n\n")

    def show_heuristic(self):
        print("Heuristics")
        for i in range(self.rows):
            print('[', end='\t')
            for j in range(self.cols):
                if self.cell[i][j].heuristic_value == -1:
                    print(" --- ", end='\t')
                else:
                    print("{:04.2F}".format(self.cell[i][j].heuristic_value), end='\t')
            print(']')
        print(end="\n\n")

    def calc_discovered(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell[i][j].state != 9:
                    self.cell[i][j].discovered = True
                else:
                    self.cell[i][j].discovered = False

    # Search for the number of undiscovered neighbours
    def calc_undiscovered_neighbours(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i != (self.rows - 1) and i != 0 and j != (self.cols - 1) and j != 0:
                    undiscovered = [i for horizontal in range(-1, 2) for vertical in range(-1, 2) if
                                    not self.cell[i + vertical][j + horizontal].discovered]

                    self.cell[i][j].undiscovered_neighbours = len(undiscovered)
                elif i == 0:
                    if j == 0:
                        undiscovered = [i for horizontal in range(0, 2) for vertical in range(0, 2) if
                                        not self.cell[i + vertical][j + horizontal].discovered]
                    elif j == (self.cols - 1):
                        undiscovered = [i for horizontal in range(-1, 1) for vertical in range(0, 2) if
                                        not self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        undiscovered = [i for horizontal in range(-1, 2) for vertical in range(0, 2) if
                                        not self.cell[i + vertical][j + horizontal].discovered]

                    self.cell[i][j].undiscovered_neighbours = len(undiscovered)

                elif j == 0:
                    if i == (self.rows - 1):
                        undiscovered = [i for horizontal in range(0, 2) for vertical in range(-1, 1) if
                                        not self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        undiscovered = [i for horizontal in range(0, 2) for vertical in range(-1, 2) if
                                        not self.cell[i + vertical][j + horizontal].discovered]

                    self.cell[i][j].undiscovered_neighbours = len(undiscovered)

                elif i == (self.rows - 1):
                    if j == (self.cols - 1):
                        undiscovered = [i for horizontal in range(-1, 1) for vertical in range(-1, 1) if
                                        not self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        undiscovered = [i for horizontal in range(-1, 2) for vertical in range(-1, 1) if
                                        not self.cell[i + vertical][j + horizontal].discovered]

                    self.cell[i][j].undiscovered_neighbours = len(undiscovered)
                else:
                    undiscovered = [i for horizontal in range(-1, 1) for vertical in range(-1, 2) if
                                    not self.cell[i + vertical][j + horizontal].discovered]

                    self.cell[i][j].undiscovered_neighbours = len(undiscovered)

                # To exclude himself
                if not self.cell[i][j].discovered:
                    self.cell[i][j].undiscovered_neighbours = self.cell[i][j].undiscovered_neighbours - 1

    # Calc heuristic as the sum of probabilities of being a mine.
    def calc_heuristic(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i != (self.rows - 1) and i != 0 and j != (self.cols - 1) and j != 0:
                    heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                 for horizontal in range(-1, 2) for vertical in range(-1, 2)
                                 if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                 and self.cell[i + vertical][j + horizontal].discovered]

                    if len(heuristic) != 0:
                        self.cell[i][j].heuristic_value = sum(heuristic)/len(heuristic)
                    else:
                        self.cell[i][j].heuristic_value = sum(heuristic)
                elif i == 0:
                    if j == 0:
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(0, 2) for vertical in range(0, 2)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]
                    elif j == (self.cols - 1):
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(-1, 1) for vertical in range(0, 2)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(-1, 2) for vertical in range(0, 2)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]

                    if len(heuristic) != 0:
                        self.cell[i][j].heuristic_value = sum(heuristic)/len(heuristic)
                    else:
                        self.cell[i][j].heuristic_value = sum(heuristic)

                elif j == 0:
                    if i == (self.rows - 1):
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(0, 2) for vertical in range(-1, 1)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(0, 2) for vertical in range(-1, 2)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]

                    if len(heuristic) != 0:
                        self.cell[i][j].heuristic_value = sum(heuristic)/len(heuristic)
                    else:
                        self.cell[i][j].heuristic_value = sum(heuristic)

                elif i == (self.rows - 1):
                    if j == (self.cols - 1):
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(-1, 1) for vertical in range(-1, 1)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]
                    else:
                        heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                     for horizontal in range(-1, 2) for vertical in range(-1, 1)
                                     if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                     and self.cell[i + vertical][j + horizontal].discovered]

                    if len(heuristic) != 0:
                        self.cell[i][j].heuristic_value = sum(heuristic)/len(heuristic)
                    else:
                        self.cell[i][j].heuristic_value = sum(heuristic)
                else:
                    heuristic = [self.cell[i + vertical][j + horizontal].state/self.cell[i + vertical][j + horizontal].undiscovered_neighbours
                                 for horizontal in range(-1, 1) for vertical in range(-1, 2)
                                 if self.cell[i + vertical][j + horizontal].undiscovered_neighbours != 0
                                 and self.cell[i + vertical][j + horizontal].discovered]
                    if len(heuristic) != 0:
                        self.cell[i][j].heuristic_value = sum(heuristic)/len(heuristic)
                    else:
                        self.cell[i][j].heuristic_value = sum(heuristic)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.cell[i][j].discovered:
                    self.cell[i][j].heuristic_value = -1

    def next_move(self):
        min_value = 100
        min_i = 0
        min_j = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.cell[i][j].discovered:
                    if (min_value > self.cell[i][j].heuristic_value) and (self.cell[i][j].heuristic_value != 0):
                        min_value = self.cell[i][j].heuristic_value
                        min_i = i
                        min_j = j

        return min_i, min_j
