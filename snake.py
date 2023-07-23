import pygame
from game import Game
from collections import deque
import random

UP = pygame.Vector2(0, -1)
DOWN = pygame.Vector2(0, 1)
LEFT = pygame.Vector2(-1, 0)
RIGHT = pygame.Vector2(1, 0)

class Snake(Game):

    def __init__(self):
        super().__init__("snake")
        self.size = 16
        self.width = 32
        self.height = 32
        
    def update(self, elapsed : float, events : list):

        self.counter += 1.0 / elapsed
        while self.counter >= 1.0 / self.speed:

            # Check if snake eats food
            if self.array[-1] == self.food:
                self.array.append(self.wrap(self.array[-1] + self.direction))
                self.food = self.randomPosition()
                self.speed += 1
                self.counter -= 1.0 / self.speed
                continue

            # Check if snake hits itself
            if self.array.__contains__(self.wrap(self.array[-1] + self.direction)):
                self.start()
                return

            # Move snake
            self.array.append(self.wrap(self.array[-1] + self.direction))
            self.array.popleft()
            self.counter -= 1.0 / self.speed

            # Handle controls
            keys = pygame.key.get_pressed()

            if self.direction is not DOWN and (keys[pygame.K_UP] or keys[pygame.K_w]):
                self.direction = UP

            elif self.direction is not UP and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.direction = DOWN
            
            elif self.direction is not RIGHT and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.direction = LEFT

            elif self.direction is not LEFT and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.direction = RIGHT

    def render(self, screen : pygame.Surface):

        # Draw food
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.food.x * self.size, self.food.y * self.size, self.size, self.size))

        # Draw snake
        for p in self.array:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(p.x * self.size, p.y * self.size, self.size, self.size))

        # Draw score
        screen.blit(pygame.font.SysFont("Arial", 24).render(str(len(self.array) - 3), True, (255, 255, 255)), (0, 0))

    def randomPosition(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.array.__contains__(pygame.Vector2(x, y)):
                return pygame.Vector2(x, y)

    def wrap(self, vector : pygame.Vector2):
        return pygame.Vector2(vector.x % self.width, vector.y % self.height)
    
    def start(self):

        # Initialise snake
        self.array : pygame.Vector2 = deque()
        self.array.append(pygame.Vector2(0, 0))
        self.array.append(pygame.Vector2(1, 0))
        self.array.append(pygame.Vector2(2, 0))

        # Initialise food
        self.food = self.randomPosition()
        
        # Initialise direction, speed, counter
        self.direction = pygame.Vector2(1, 0)
        self.speed = 10
        self.counter = 0

    def pause(self):
        pass

    def resume(self):
        pass

    def quit(self):
        pass

