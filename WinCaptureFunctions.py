from PIL import ImageGrab
from time import sleep
from Board_lib import Board
import win32gui, win32api, win32con
import sys
import subprocess
import ctypes
import cv2
import numpy as np
import gc


handler = -1
SCREEN_WIDTH, SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)


def loadWindowsList(hwnd,toplist):
    toplist.append((hwnd, win32gui.GetWindowText(hwnd)))



def loadTemplate(paths):  # This function load and modify the template images
    template = []
    for path in paths:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (t, thresh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        template.append(thresh)
    return template


def loadBoard(name):  # This function capture and crop the Minesweeper screen
    #print('LoadBoard')
    recover_focus('buscaminas')

    image = windowCapture(name)

    # Convert PIL to OpenCV
    open_cv_image = np.array(image)
    board = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
    board_cropped = board[101:-11, 15:-11]  # Crop the image to extract the board
    return board_cropped


def getHwnd(name):  # This function obtains the hwnd of the window with the provided name
    global handler
    toplist =[]
    #if handler == -1:
    win32gui.EnumWindows(loadWindowsList, toplist)
    #print(len(toplist))
    window = [(hwnd, title) for hwnd, title in toplist if name in title.lower()]
    handler = window[0][0]

    gc.collect()
    return handler


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
        if not (np.bitwise_xor(image, template[i]).any()):
            return i
    return None


def obtainMatrix(board, template):  # This function returns a matrix reflecting the state of the game
    #print("Obtain matrix")
    # CV treatment of the image
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    (t, thresh) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Debugging
    # cv2.imshow("thresH", thresh)
    # cv2.waitKey()

    (boardHeight, boardWidth) = board.shape[:2]

    board_mat = np.zeros((int(boardHeight/ 16), int(boardWidth / 16)))
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


def getBoard(template):  # This function returns the position of the window with the provided hwnd
    # Obtaining the matrix that reflects the state of the game
    image = loadBoard('buscaminas')
    return obtainMatrix(image, template)


def mouse(x, y, action=False):  # This function controls the mouse (action is usually disabled for debugging)
    # print('mouse')
    recover_focus('buscaminas')

    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x / SCREEN_WIDTH * 65535.0),
                         int(y / SCREEN_HEIGHT * 65535.0))
    if action:
        # Click of the mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)



def ask4cords():


    raw_input = input('Introduzca coordenadas (fila, columna) del bloque a clickar:')

    try:
        row, col = raw_input.split()

    except:
        try:
            row, col = raw_input.split(',')

        except:
            try:
                row, col = raw_input.split('.')

            except:
                print("Te has esforzado, pero la has cagado")
                return -1,-1

    return int(row), int(col)


def click_board(x, y):
    # Obtaining the position of the Minesweeper window
    # print('click Board')
    recover_focus('buscaminas')

    x1, _, y1, _ = getPosition(getHwnd('buscaminas'), None)

    # Moving the mouse to a certain box
    dx = 22 + 16 * x
    dy = 108 + 16 * y
    mouse(x1 + dx, y1 + dy, action=True)  # (x,y)


def init_template():
    # Path of the template images
    paths = [r'.\data\0.png', r'.\data\1.png', r'.\data\2.png', r'.\data\3.png', r'.\data\4.png', r'.\data\5.png',
             r'.\data\6.png', r'.\data\7.png', r'.\data\8.png', r'.\data\block.png', r'.\data\flag.png',
             r'.\data\bomb.png', r'.\data\bomb_2.png', r'.\data\bomb_3.png']

    '''# Number of bombs surrounding the box
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
    paths.append(r'.\data\bomb_3.png')  # 13'''

    # Loading of all the templates
    template = loadTemplate(paths)

    return template


def init_game():
    template = init_template()
    # Obtaining the matrix that reflects the state of the game
    image = loadBoard('buscaminas')
    print(image.shape)
    mat = obtainMatrix(image, template)
    print(mat.shape)
    row, column = mat.shape
    board = Board(row, column)
    board.new_game()
    return board


def recover_focus(name):
    # To get back window in focus
    try:
        hwnd = getHwnd(name)
        win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
        win32gui.SetForegroundWindow(hwnd)

    except:
        print("Are you sure close window is?")