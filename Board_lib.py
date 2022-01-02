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
        row_list = [Cell(False, 9, 0) for i in range(rows)]
        self.cell = [copy.deepcopy(row_list) for j in range(columns)]
        # Obtaining the initial state of the board
        template = wcf.init_template()
        self.update_board(template)

    def new_game(self, template):
        # Clicking the board to start new game
        wcf.click_board(int(self.cols/2), -2)
        self.update_board(template)
        self.solved = False
        self.dead = False

    def check_dead(self):
        idx = np.argwhere(self.obtain_matrix() == 11)
        dead = True if idx.shape[0] != 0 else False
        return dead

    def update_board(self, template):
        # Obtaining the matrix that reflects the state of the game
        board_image = wcf.loadBoard('buscaminas')
        mat = wcf.obtainMatrix(board_image, template)

        # update contains the coordinates which has changed in this iteration
        update = np.argwhere(self.obtain_matrix() - mat)
        for idx in update:
            # This loop updates every cell state which has changed
            row, col = idx[0], idx[1]
            self.cell[row][col].update_state(int(mat[row][col]))

        # Updating the dead state
        self.dead = self.check_dead()

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
