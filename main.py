import WinCaptureFunctions as wcf
import DatasetGenerator as dsg


def main():
    # Loading of the Minesweeper board
    board, template = wcf.init_game()

    # Test of printing a random board solved
    # print(dsg.generate_board(7,10,20))

    while True:
        board.update_board(template)
        #wcf.click_board(-1, -1)
        board.show_board()

        print(board.check_dead())

        while True:
            try:
                # Coordinates of the box to click
                row, col = wcf.ask4cords()
                break

            except ValueError:
                print('Invalid Input. Try again.')

        # Clicking the board
        wcf.click_board(col, row)

if __name__ == "__main__":
    main()

