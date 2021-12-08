import WinCaptureFunctions as wcf


def main():

    template = wcf.init_template()

    while True:
        # Loading of the Minesweeper board
        board = wcf.loadBoard('buscaminas')

        # Obtaining the matrix which represents the state of the game
        game_mat = wcf.obtainMatrix(board, template)
        print(game_mat)

        # Coordinates of the box to click
        x, y = wcf.ask4cords()

        # Clicking the board
        wcf.click_board(x, y)


if __name__ == "__main__":
    main()

