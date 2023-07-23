import pygame
import random
from collections import deque
from game import Game

I_tetromino = [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

J_tetromino = [
    [2, 0, 0],
    [2, 2, 2],
    [0, 0, 0]
]

L_tetromino = [
    [0, 0, 3],
    [3, 3, 3],
    [0, 0, 0]
]

O_tetromino = [
    [4, 4],
    [4, 4]
]

S_tetromino = [
    [0, 5, 5],
    [5, 5, 0],
    [0, 0, 0]
]

T_tetromino = [
    [0, 6, 0],
    [6, 6, 6],
    [0, 0, 0]
]

Z_tetromino = [
    [7, 7, 0],
    [0, 7, 7],
    [0, 0, 0]
]

tetrominoes = [ I_tetromino, J_tetromino, L_tetromino, O_tetromino, S_tetromino, T_tetromino, Z_tetromino ]

def rotate_cw(tetromino: list):
    return [ [ tetromino[y][x] for y in range(len(tetromino)) ] for x in range(len(tetromino[0]) - 1, -1, -1) ]

def rotate_ccw(tetromino: list):
    return [ [ tetromino[y][x] for y in range(len(tetromino) - 1, -1, -1) ] for x in range(len(tetromino[0])) ]

def random_tetromino():
    return tetrominoes[random.randint(0, len(tetrominoes) - 1)]

def color(value):
    if value == 0:
        return (0, 0, 0)
    elif value == 1:
        return (0, 255, 255)
    elif value == 2:
        return (0, 0, 255)
    elif value == 3:
        return (255, 165, 0)
    elif value == 4:
        return (255, 255, 0)
    elif value == 5:
        return (0, 255, 0)
    elif value == 6:
        return (128, 0, 128)
    elif value == 7:
        return (255, 0, 0)

class Tetris(Game):

    def __init__(self):
        super().__init__("tetris")
        self.size = 16
        self.width = 32
        self.height = 32
      
    def start(self):
        self.counter = 0
        self.speed = 1
        self.size = 16
        self.width = 10
        self.height = 20    
        self.board = [ [ 0 for x in range(self.width) ] for y in range(self.height) ]
        self.x = 5
        self.y = 0
        self.queue = deque()
        self.queue.append(random_tetromino())
        self.queue.append(random_tetromino())
        self.queue.append(random_tetromino())

    def update(self, elapsed : float, events : list):
        self.counter += 1.0 / elapsed
        while self.counter >= 1.0 / self.speed:
            if self.collide(self.queue[0], self.x, self.y + 1):
                for i in range(len(self.queue[0])):
                    for j in range(len(self.queue[0][i])):
                        if self.queue[0][i][j] != 0:
                            self.board[self.y + i][self.x + j] = self.queue[0][i][j]
                self.queue.popleft()
                self.queue.append(random_tetromino())
                self.x = 5
                self.y = 0
                self.speed += 0.1
                continue
            self.y += 1
            self.counter -= 1.0 / self.speed

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not self.collide(rotate_cw(self.queue[0]), self.x, self.y):
                        self.queue[0] = rotate_cw(self.queue[0])

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.collide(self.queue[0], self.x, self.y + 1):
                        self.y += 1
                    #if not self.collide(rotate_ccw(self.queue[0]), self.x, self.y):
                    #    self.queue[0] = rotate_ccw(self.queue[0])
                
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not self.collide(self.queue[0], self.x - 1, self.y):
                        self.x -= 1
                
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not self.collide(self.queue[0], self.x + 1, self.y):
                        self.x += 1

    def collide(self, tetromino: list, x: int, y: int):

        for i in range(len(tetromino)):
            for j in range(len(tetromino[i])):
                if tetromino[i][j] != 0:

                    if x + j < 0 or x + j >= self.width:
                        return True
                    
                    if y + i >= self.height:
                        return True
                    
                    if self.board[y + i][x + j] != 0:
                        return True
        return False

    def render(self, screen : pygame.Surface):
        
        # draw border
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, self.width * self.size, self.height * self.size), 1)

        # draw board
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 0:
                    pygame.draw.rect(screen, color(self.board[y][x]), pygame.Rect(x * self.size, y * self.size, self.size, self.size))

        # draw current tetromino
        for y in range(len(self.queue[0])):
            for x in range(len(self.queue[0][0])):
                if self.queue[0][y][x] != 0:
                    pygame.draw.rect(screen, color(self.queue[0][y][x]), pygame.Rect((self.x + x) * self.size, (self.y + y) * self.size, self.size, self.size))

        # draw queue
        for i in range(len(self.queue)):
            for y in range(len(self.queue[i])):
                for x in range(len(self.queue[i][0])):
                    if self.queue[i][y][x] != 0:
                        pygame.draw.rect(screen, color(self.queue[i][y][x]), pygame.Rect((self.width + 2 + x) * self.size, (i * 4 + y) * self.size, self.size, self.size))