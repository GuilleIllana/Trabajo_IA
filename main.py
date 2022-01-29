import WinCaptureFunctions as wcf
import win32api
import gc
import time
import MS_eq_solver as mses




def main():
    # In order to configure difficulty, start minesweeper game and
    # change the settings. Then run python script

    """
    ############################################################
    #-------------            PARAMETERS       ----------------#
    ############################################################
    """

    # Whether or not use model checking
    model_checking = 1
    # Stop when winning
    stop_winning = 1
    # Whether or not showing data
    show_data = 1
    # Maximum number of games
    n_partidas = 100

    """
    ############################################################
    #-------------            GAME          -------------------#
    ############################################################
    """
    # Loading of the Minesweeper board
    board = wcf.init_game()


    partidas = 0
    resultados = []
    while partidas < n_partidas:

        # IN ORDER TO PAUSE THE GAME PRESS F6
        state = win32api.GetKeyState(117)
        while state:
            state = win32api.GetKeyState(117)
        gc.collect()

        if show_data:
            if not model_checking:
                board.show_heuristic()
            board.show_board()

        # if it loses restart the game
        if board.check_dead():
            resultados.append(0)
            partidas = partidas + 1
            print('partida ', partidas, ' de ', n_partidas, ', victorias: ', resultados.count(1))
            if partidas == n_partidas:
                break

            board = wcf.init_game()
            board.new_game()

        if board.check_solved():
            resultados.append(1)
            partidas = partidas + 1
            print('partida ', partidas, ' de ', n_partidas, ', victorias: ', resultados.count(1))
            if partidas == n_partidas:
                break
            if stop_winning:
                return
            board = wcf.init_game()
            board.new_game()
            start_time = time.time()

        # Clicking the board
        board.update_board()

        if model_checking:
            move, i, j = mses.get_move_model_checking(board)

            if move == 1:
                continue

        # If no solution, then play the heuristic
        i, j = board.next_move()
        wcf.click_board(j, i)

    ganadas = (resultados.count(1)/n_partidas)*100
    perdidas = (resultados.count(0)/n_partidas)*100


    print("Se ha ganado un " + str(ganadas)+"% y se ha perdido un " + str(perdidas)+"% de "+str(n_partidas)+" partidas")


if __name__ == "__main__":
    main()


