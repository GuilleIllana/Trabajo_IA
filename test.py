from Board_lib import Board
import WinCaptureFunctions as wcf


Tablero = Board(9,9)

print(Tablero.cell[0][0].state)

template = wcf.init_template()

Tablero.show_board()

Tablero.update_board(template)

Tablero.show_board()

#Tablero.show_discovered()