from PIL import ImageGrab
from time import sleep
import win32gui, win32api, win32con
import sys
import subprocess
import ctypes
import cv2
import numpy as np

toplist, winlist = [], []
SCREEN_WIDTH, SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def loadWindowsList(hwnd, toplist):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


def loadTemplate(paths):  # This function load and modify the template images
    template = []
    for path in paths:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (t, thresh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        template.append(thresh)
    return template


def loadBoard(name):  # This function capture and crop the Minesweeper screen
    image = windowCapture(name)

    # Convert PIL to OpenCV
    open_cv_image = np.array(image)
    board = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    board_cropped = board[101:-11, 15:-11]  # Crop the image to extract the board
    return board_cropped


def getHwnd(name):  # This function obtains the hwnd of the window with the provided name
    win32gui.EnumWindows(loadWindowsList, toplist)
    window = [(hwnd, title) for hwnd, title in winlist if name in title.lower()]
    return window[0][0]


def windowCapture(name):  # This function returns an image of the provided window name, in this case, Minesweeper
    try:
        hwnd = getHwnd(name)
        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        return img

    except:
        # If Minesweeper can't be found, this code executes it
        print('Minesweeper not found. Executing Minesweeper...')
        try:
            subprocess.Popen(r".\Buscaminas.exe")
            sleep(1)

            hwnd = getHwnd(name)
            win32gui.SetForegroundWindow(hwnd)
            bbox = win32gui.GetWindowRect(hwnd)
            img = ImageGrab.grab(bbox)
            return img

        except:
            sys.exit("Minesweeper couldn't be open")


def boxCheck(image, template):  # This function checks the board searching for known figures
    for i in range(len(template)):
        if not(np.bitwise_xor(image, template[i]).any()):
            return i
    return None


def obtainMatrix(board, template):  # This function returns a matrix reflecting the state of the game
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
            # Debugging
            """if i == 0 and j == 0:
                print(state)
                cv2.imshow("bloque", box)
                cv2.waitKey(0)"""
    return board_mat


def getPosition(hwnd, extra):  # This function returns the position of the window with the provided hwnd
    rect = win32gui.GetWindowRect(hwnd)
    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    return x1, x2, y1, y2


def mouse(x, y, side=0 , action=False):  # This function controls the mouse (action is usually disabled for debugging)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x / SCREEN_WIDTH * 65535.0),
                         int(y / SCREEN_HEIGHT * 65535.0))
    if action and side == 0:
        # Click of the mouse (LEFT)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    elif action and side == 1:
        # Click of the mouse (RIGHT)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def main():
    # Path of the template images
    paths = []

    # Number of bombs surrounding the box
    paths.append(r'.\data\0.png')  # 0
    paths.append(r'.\data\1.png')  # 1
    paths.append(r'.\data\2.png')  # 2
    paths.append(r'.\data\3.png')  # 3
    paths.append(r'.\data\4.png')  # 4
    paths.append(r'.\data\5.png')  # 5
    paths.append(r'.\data\6.png')  # 6
    paths.append(r'.\data\7.png')  # 7
    paths.append(r'.\data\8.png')  # 8

    # Unknown block
    paths.append(r'.\data\block.png')  # 9

    # Flag
    paths.append(r'.\data\flag.png')  # 10

    # Bomb
    paths.append(r'.\data\bomb.png')  # 11

    # Bomb with flag on top
    paths.append(r'.\data\bomb_2.png')  # 12

    # Bomb which has exploded
    paths.append(r'.\data\bomb_3.png')  # 13

    # Loading of all the templates
    template = loadTemplate(paths)

    # Loading of the Minesweeper board
    board = loadBoard('buscaminas')

    # Obtaining the matrix which represents the state of the game
    game_mat = obtainMatrix(board, template)
    print(game_mat)

    # Coordinates of the box to click
    x = int(input('Introduzca coordenada x del bloque a clickar:'))
    y = int(input('Introduzca coordenada y del bloque a clickar:'))

    # Obtaining the position of the Minesweeper window
    x1, _, y1, _ = getPosition(getHwnd('buscaminas'), None)

    # Moving the mouse to a certain box
    dx = 22 + 16 * x
    dy = 108 + 16 * y
    mouse(x1+dx, y1+dy, side=0, action=True) # (x,y)

if __name__ == "__main__":
    main()

