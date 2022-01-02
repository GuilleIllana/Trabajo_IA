from Board_lib import Board
import WinCaptureFunctions as wcf

def init():
    template = wcf.init_template()
    # Obtaining the matrix that reflects the state of the game
    image = wcf.loadBoard('buscaminas')
    mat = wcf.obtainMatrix(image, template)
    row, column = mat.shape
    Tablero = Board(row, column)
    return Tablero, template


Tablero, template = init()

Tablero.show_board()

Tablero.update_board(template)

Tablero.show_board()

Tablero.show_discovered()