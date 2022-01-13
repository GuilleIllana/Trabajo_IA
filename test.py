import WinCaptureFunctions as wcf
import Board_lib
import DatasetGenerator as dsg
import win32api
import gc
import time
import MS_eq_solver as mses
import numpy as np
#from bitstring import BitStream, BitArray

#board = wcf.init_game()
#board.update_board()
#
#input("Pulse cualquier tecla para continuar")
#
#board.update_board()
#mat = np.array(mses.expanded_board(board))
#
#
#for i in range(board.rows):
#    for j in range(board.cols):
#        if mat[i+1][j+1] == 0 or mat[i+1][j+1] == 9 or mat[i+1][j+1] == 10 or mat[i+1][j+1] == 15:
#            continue
#        r,c,m = mses.solve_system_1(mat, i, j)
#        if m == 0:
#            wcf.click_board(r-1, c-1)
#            print('no mina', r-1, c-1)
#        elif m == 1:
#            wcf.click_board_right(r - 1, c - 1)
#            print('mina', r-1, c-1)
#
#        print(i, j)
#
#board.update_board()
##board.show_board()
#
#print(mat)





