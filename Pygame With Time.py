import pygame
import threading
from queue import Queue, LifoQueue, PriorityQueue
import time

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
INDIGO = (75,0,130)

escape_pressed = True
algorithm_running = False
startTime = 0

maze1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, "S", 0, 0, 1, 1, 1, 1, 0, 0, 0,0 ],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 4, 1, 1, 1, 1, 1, 0, 12, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 10, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, "G", 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

maze2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, "S", 1, 1, 1, 1, 1, 1, 1, 2, 2, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, "G", 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

maze3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 'S', 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 'G', 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

maze4 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 'S', 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 'G', 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

maze5 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 'G', 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

maze6 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 'S', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 'G', 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def find_start_and_target(grid):
    start = None
    target = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "G":
                target = (r, c)
    return start, target

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Maze Navigation")

stop_event = threading.Event()

font = pygame.font.SysFont('Arial', 30)

def show_message(message, sub_message ):
    """Displays a message on the screen."""
    
    screen.fill(WHITE)
    
    Tital = "Maze Navigation"
    sub_message2 = "Mostafa Abdallah 192100058                  Sherif Diaa 192100037"
    sub_message4 = "Dr. Rasha Saleh                                                  Eng. Hager Rabea" 
       
    tital_text = font.render(Tital, True, GRAY)
    main_text = font.render(message, True, GRAY)
    sub_text = font.render(sub_message, True, GRAY)
    sub_text2 = font.render(sub_message2, True, GRAY)
    sub_text3 = font.render(sub_message4, True, GRAY)

    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    tital_ract = tital_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 250))
    main_rect = main_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
    sub_rect2 = sub_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    sub_rect3 = sub_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300))

    screen.blit(tital_text, tital_ract)
    screen.blit(main_text, main_rect)
    screen.blit(sub_text, sub_rect)
    screen.blit(sub_text2, sub_rect2)
    screen.blit(sub_text3, sub_rect3)
    
    pygame.display.update()

def update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT):
    global CELL_SIZE
    ROWS = len(grid)
    COLS = len(grid[0])
    if (ROWS > 20) or (COLS > 20):
        CELL_SIZE = min(SCREEN_WIDTH // ROWS, SCREEN_HEIGHT // COLS) + 10
    else:
        CELL_SIZE = min(SCREEN_WIDTH // ROWS, SCREEN_HEIGHT // COLS) - 10
    SCREEN_HEIGHT = ROWS * CELL_SIZE + 30
    SCREEN_WIDTH = COLS * CELL_SIZE
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def get_neighbors(node, grid):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        nr, nc = node[0] + dr, node[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(parent, start, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent.get(current)
    return path if path and path[-1] == start else []

def bfs(grid, start, target, stop_event):
    queue = Queue()
    queue.put(start)
    visited = set()
    visited.add(start)
    parent = {start: None}
    expanded_nodes = set()

    while not queue.empty():
        if stop_event.is_set():
            break
        
        current = queue.get()
        if current == target:
            break
        
        expanded_nodes.add(current)
        
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.put(neighbor)
                parent[neighbor] = current
        
        visualize_grid(grid, visited, parent, start, target, expanded_nodes, algorithm="BFS")
        pygame.time.delay(200)
    
    final_path = reconstruct_path(parent, start, target)
    visualize_grid(grid, visited, parent, start, target, expanded_nodes, final_path, step_by_step=True, algorithm="BFS")

def dfs(grid, start, target, stop_event):
    stack = LifoQueue()
    stack.put(start)
    visited = set()
    visited.add(start)
    parent = {start: None}
    expanded_nodes = set()

    while not stack.empty():
        if stop_event.is_set():  
            break
        
        current = stack.get()
        if current == target:
            break
        
        expanded_nodes.add(current)
        
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.put(neighbor)
                parent[neighbor] = current
        
        visualize_grid(grid, visited, parent, start, target, expanded_nodes, algorithm="DFS")
        pygame.time.delay(200)
    
    final_path = reconstruct_path(parent, start, target)
    visualize_grid(grid, visited, parent, start, target, expanded_nodes, final_path, step_by_step=True, algorithm="DFS")

def ucs(grid, start, target, stop_event):
    pq = PriorityQueue()
    pq.put((0, start))
    visited = set()
    parent = {start: None}
    cost = {start: 0}
    expanded_nodes = set()

    while not pq.empty():
        if stop_event.is_set():
            break

        current_cost, current = pq.get()
        if current == target:
            break

        if current in visited:
            continue

        visited.add(current)
        expanded_nodes.add(current)
        
        for neighbor in get_neighbors(current, grid):
            try:
                new_cost = current_cost + int(grid[neighbor[0]][neighbor[1]])
            except ValueError:
                new_cost = current_cost + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                pq.put((new_cost, neighbor))
                parent[neighbor] = current

        expanded_nodes.add(current)

        visualize_grid(grid, visited, parent, start, target, expanded_nodes, algorithm="UCS")
        pygame.time.delay(200)

    final_path = reconstruct_path(parent, start, target)
    visualize_grid(grid, visited, parent, start, target, expanded_nodes, final_path, step_by_step=True, algorithm="UCS")

def visualize_grid(grid, visited, parent, start, target, expanded_nodes, final_path=None, step_by_step=False, algorithm=""):
    if final_path is None:
        final_path = []

    screen.fill(BLACK)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            try:
                value = int(grid[r][c])
            except ValueError:
                value = 1

            color = WHITE if value != 0 else BLACK
            if value > 1:
                color = INDIGO

            if (r, c) in final_path:
                color = YELLOW
            elif (r, c) in expanded_nodes:
                color = GRAY
            elif (r, c) in visited:
                color = BLUE

            pygame.draw.rect(screen, color, pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + 30, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + 30, CELL_SIZE, CELL_SIZE), 1)

    pygame.draw.circle(screen, RED, (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2 + 30), CELL_SIZE // 4)
    pygame.draw.circle(screen, GREEN, (target[1] * CELL_SIZE + CELL_SIZE // 2, target[0] * CELL_SIZE + CELL_SIZE // 2 + 30), CELL_SIZE // 4)

    text_background_rect = pygame.Rect(10, 10, 400, 30)
    pygame.draw.rect(screen, BLACK, text_background_rect)

    if algorithm_running and not step_by_step:
        running_time_text = font.render(f"Time: {time.time() - startTime:.1f}s", True, GRAY)
    else:
        running_time_text = font.render("Time: 0.0s", True, GRAY)

    screen.blit(running_time_text, (10, 10))
    screen.blit(font.render("Algorithm: " + algorithm, True, GRAY), (200, 10))

    pygame.display.update()

    if step_by_step:
        for i in range(len(final_path)):
            visualize_grid(grid, visited, parent, start, target, expanded_nodes, final_path[:i+1], algorithm=algorithm)
            pygame.time.delay(100)
            pygame.display.update()
            pygame.event.pump()

def stop_algorithm():
    global algorithm_running
    algorithm_running = False
    stop_event.set()

def run_algorithm(algorithm):
    global algorithm_running, startTime
    if algorithm_running:
        return 
    algorithm_running = True
    stop_event.clear()  
    start, target = find_start_and_target(grid) 
    try:
        startTime = time.time()
        if algorithm == "BFS":
            bfs(grid, start, target, stop_event)
        elif algorithm == "DFS":
            dfs(grid, start, target, stop_event)
        elif algorithm == "UCS":
            ucs(grid, start, target, stop_event)
    finally:
        algorithm_running = False

def main():
    running = True
    clock = pygame.time.Clock()
    
    global grid
    grid = maze1
    show_message("Choose Maze 1 or 2 or 3 or 4 or 5 or 6", "Press 'b' for BFS, 'd' for DFS, 'u' for UCS, Press 's' to stop the algorithm")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global escape_pressed
                    if not escape_pressed:
                        stop_algorithm()
                        pygame.time.delay(200)
                        show_message("Choose Maze 1 or 2 or 3 or 4 or 5 or 6", "Press 'b' for BFS, 'd' for DFS, 'u' for UCS, Press 's' to stop the algorithm")
                        escape_pressed = True
                    else:
                        running = False
                elif event.key == pygame.K_b and not algorithm_running and not escape_pressed:
                    threading.Thread(target=run_algorithm, args=("BFS",), daemon=True).start()
                elif event.key == pygame.K_d and not algorithm_running and not escape_pressed:
                    threading.Thread(target=run_algorithm, args=("DFS",), daemon=True).start()
                elif event.key == pygame.K_u and not algorithm_running and not escape_pressed:
                    threading.Thread(target=run_algorithm, args=("UCS",), daemon=True).start()
                elif event.key == pygame.K_s and not escape_pressed:
                    stop_algorithm()
                elif event.key == pygame.K_0 and not algorithm_running:
                    grid = [[1 for _ in range(10)] for _ in range(10)]
                    grid[0][0] = "S"
                    grid[-1][-1] = "G"
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_1 and not algorithm_running:
                    grid = maze1
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_2 and not algorithm_running:
                    grid = maze2
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_3 and not algorithm_running:
                    grid = maze3
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_4 and not algorithm_running:
                    grid = maze4
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_5 and not algorithm_running:
                    grid = maze5
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                elif event.key == pygame.K_6 and not algorithm_running:
                    grid = maze6
                    update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)                
                    start, target = find_start_and_target(grid)
                    visualize_grid(grid, set(), {}, start, target, set())
                # elif event.key == pygame.K_7 and not algorithm_running:
                #     grid = maze7
                #     update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)                
                #     start, target = find_start_and_target(grid)
                #     visualize_grid(grid, set(), {}, start, target, set())
                # elif event.key == pygame.K_8 and not algorithm_running:
                #     grid = maze8
                #     update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                #     start, target = find_start_and_target(grid)
                #     visualize_grid(grid, set(), {}, start, target, set())
                # elif event.key == pygame.K_9 and not algorithm_running:
                #     grid = maze9
                #     update_screen_dimensions(grid, SCREEN_WIDTH, SCREEN_HEIGHT)
                #     start, target = find_start_and_target(grid)
                #     visualize_grid(grid, set(), {}, start, target, set())
                
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE and not algorithm_running and event.key != pygame.K_b and event.key != pygame.K_d and event.key != pygame.K_u and event.key != pygame.K_s:
                escape_pressed = False

        clock.tick(60)
    
    pygame.quit()

main()
