import WinCaptureFunctions as wcf
import DatasetGenerator as dsg
import time
import win32api
import gc



def main():
    # Loading of the Minesweeper board
    board = wcf.init_game()

    # Test of printing a random board solved
    # print(dsg.generate_board(7,10,20))

    while True:

        #wcf.click_board(-1, -1)
        board.show_board()


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
        board.show_heuristic()
        print(board.next_move())
        i, j = board.next_move()
        wcf.click_board(j, i)

        # if it looses restart the game
        if board.check_dead():
            print("LA PALMASTE")

            board = wcf.init_game()
            board.new_game()
            #wcf.click_board(5, 5)

        if board.check_solved():
            print("LA GANASTE")
            break


        # PARA PAUSAR PULSAR EL F6
        state = win32api.GetKeyState(117)
        while state:
            state = win32api.GetKeyState(117)
        gc.collect()
if __name__ == "__main__":
    main()

