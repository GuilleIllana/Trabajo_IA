import WinCaptureFunctions as wcf
import DatasetGenerator as dsg


def main():
    # Loading of the Minesweeper board
    board = wcf.init_game()

    # Test of printing a random board solved
    # print(dsg.generate_board(7,10,20))
    board.update_board()
    while True:

        #wcf.click_board(-1, -1)
        board.show_board()


        while True:
            try:
                # Coordinates of the box to click
                row, col = wcf.ask4cords()
                break

            except ValueError:
                print('Invalid Input. Try again.')

        # Clicking the board
        wcf.click_board(col, row)
        board.update_board()
        board.show_undiscovered_neighbours()
        board.show_heuristic()

        if board.check_dead():
            _garbage = input("Press Enter to continue...")
            board = wcf.init_game()
            board.new_game()

if __name__ == "__main__":
    main()

