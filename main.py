from PIL import ImageGrab
import win32gui
from time import sleep
import subprocess
import cv2
import numpy as np

toplist, winlist = [], []


def loadWindowsList(hwnd, toplist):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


def loadTemplate(paths):
    template = []
    for path in paths:
        template.append(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY))
    return template


def loadBoard(name):
    # Capturing the Minesweeper screen
    image = windowCapture(name)

    # Convert PIL to OpenCV
    open_cv_image = np.array(image)
    board = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    board_cropped = board[101:-11, 15:-11]  # Crop the image to extract the board
    return board_cropped


def windowCapture(name):
    # This function return an image of the Minesweeper tab
    try:
        win32gui.EnumWindows(loadWindowsList, toplist)
        window = [(hwnd, title) for hwnd, title in winlist if name in title.lower()]

        hwnd = window[0][0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        return img

    # If Minesweeper can't be found, this code executes it
    except:
        subprocess.Popen("D:\\Guillermo\\Documentos\\Universidad\\Inteligencia artificial\\Trabajo_IA\\Buscaminas.exe")
        sleep(1)

        win32gui.EnumWindows(loadWindowsList, toplist)
        window = [(hwnd, title) for hwnd, title in winlist if name in title.lower()]

        hwnd = window[0][0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        return img


def boxCheck(image,template):
    # Checks the board searching for known figures
    for i in range(len(template)):
        if not(np.bitwise_xor(image, template[i]).any()):
            return i
    return None


def obtainMatrix(board, template):
    # CV treatment of the image
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    (t, thresh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Debugging
    #cv2.imshow("thresH", thresh)
    #cv2.waitKey()

    (boardHeight, boardWidth) = board.shape[:2]
    board_mat = np.zeros((int(boardHeight / 16), int(boardWidth / 16)))
    for i in range(int(boardHeight / 16)):
        for j in range(int(boardWidth / 16)):
            box = thresh[16 * i:16 * i + 16, 16 * j:16 * j + 16]  # Crop the image to extract the board
            state = boxCheck(box, template)
            board_mat[i][j] = state
            """No detecta los bloques con bandera, bomba roja (explotada) ni el número 3"""
            # Debugging
            #if i == 6 and j == 2:
                #print(state)
                #cv2.imshow("bloque", box)
                #cv2.waitKey(0)
    return board_mat


def main():
    # Path of the template images
    paths = []
    paths.append(r'.\data\0.png')
    paths.append(r'.\data\1.png')
    paths.append(r'.\data\2.png')
    paths.append(r'.\data\3.png')
    paths.append(r'.\data\4.png')
    paths.append(r'.\data\5.png')
    paths.append(r'.\data\6.png')
    paths.append(r'.\data\7.png')
    paths.append(r'.\data\8.png')
    paths.append(r'.\data\block.png')
    paths.append(r'.\data\flag.png')
    paths.append(r'.\data\bomb.png')
    paths.append(r'.\data\bomb_red.png')

    # Loading of all the templates
    template = loadTemplate(paths)

    # Loading of the Minesweeper board
    board = loadBoard('buscaminas')

    # Obtain the matrix which represents the state of the game
    game_mat = obtainMatrix(board, template)
    print(game_mat)

if __name__ == "__main__":
    main()

