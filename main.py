import WinCaptureFunctions as wcf
import DatasetGenerator as dsg
def main():

    template = wcf.init_template()

    # Test of printing a random board solved
    print(dsg.generate_board(7,10,20))

    while True:
        # Loading of the Minesweeper board
        board = wcf.loadBoard('buscaminas')
        wcf.click_board(-1,-1)

        # Obtaining the matrix which represents the state of the game
        game_mat = wcf.obtainMatrix(board, template)
        print(game_mat)

        # Coordinates of the box to click
        x, y = wcf.ask4cords()

        # Clicking the board
        wcf.click_board(x, y)



if __name__ == "__main__":
    main()

