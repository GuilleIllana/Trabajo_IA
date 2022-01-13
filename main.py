import WinCaptureFunctions as wcf
import DatasetGenerator as dsg
import win32api
import gc
import time
import MS_eq_solver as mses
import numpy as np

import test


def main():
    # Loading of the Minesweeper board
    board = wcf.init_game()

    # Test of printing a random board solved
    # print(dsg.generate_board(7,10,20))
    start_time = time.time()

    n_partidas = 10
    partidas = 0
    resultados = []
    while partidas < n_partidas:

        #wcf.click_board(-1, -1)
        #board.show_board()


        '''while True:
            try:
                # Coordinates of the box to click
                row, col = wcf.ask4cords()
                break

            except ValueError:
                print('Invalid Input. Try again.')
        '''
        # Clicking the board

        board.update_board()
        # board.show_undiscovered_neighbours()
        #board.show_heuristic()
        # print(board.next_move())
        mat = np.array(mses.expanded_board(board))

        #print('mat')
        move = 0
        i = 0
        j = 0
        #print(board.rows)
        #print(board.cols)
        while i < board.rows and move == 0:
            j = 0
            while j < board.cols and move == 0:
                #print(i, j)
                if mat[i + 1][j + 1] == 0 or mat[i + 1][j + 1] == 9 or mat[i + 1][j + 1] == 10 or mat[i + 1][
                    j + 1] == 15:
                    j = j + 1
                    continue
                r, c, m = mses.solve_system_1(mat, i, j)
                if m == 0:
                    wcf.click_board(c - 1, r - 1)
                    #time.sleep(0.2)
                    #print('no mina', r - 1, c - 1)
                    move = 1
                elif m == 1:
                    wcf.click_board_right(c - 1, r - 1)
                    #time.sleep(0.2)
                    #print('mina', r - 1, c - 1)
                    move = 1
                j = j + 1
            i = i + 1

        if move == 0:
            i, j = board.next_move()
            wcf.click_board(j, i)

        # if it looses restart the game
        if board.check_dead():
            print("Perdiste!")
            print("--- Perdiste en %s segundos ---" % (time.time() - start_time))
            print("\n")
            board.show_board()

            resultados.append(0)
            partidas = partidas + 1
            board = wcf.init_game()
            board.new_game()
            start_time = time.time()


            #wcf.click_board(5, 5)

        if board.check_solved():
            print("Has ganado")
            print("--- GANASTE en %s segundos ---" % (time.time() - start_time))
            print("\n")
            
            board.show_board()

            resultados.append(1)
            partidas = partidas + 1
            board = wcf.init_game()
            board.new_game()
            start_time = time.time()



        # PARA PAUSAR PULSAR EL F6
        state = win32api.GetKeyState(117)
        while state:
            state = win32api.GetKeyState(117)
        gc.collect()

    ganadas = (resultados.count(1)/n_partidas)*100
    perdidas = (resultados.count(0)/n_partidas)*100

    print("Se ha ganado un " + str(ganadas)+"% y se ha perdido un " + str(perdidas)+"% de "+str(n_partidas)+" partidas")


if __name__ == "__main__":
    main()


