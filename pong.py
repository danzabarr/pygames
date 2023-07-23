import pygame
import math
import random
from game import Game

class Pong(Game):
        
    def __init__(self):
        super().__init__("pong")
        self.paddle_width = 16
        self.paddle_height = 64
        self.ball_size = 16

    def start(self):
        self.ball = pygame.Vector2(self.paddle_width, 256)
        angle = random.uniform(-math.pi / 4, math.pi / 4)
        velocity = 64
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * velocity
        self.p1 = 256
        self.p2 = 256
        self.p1_score = 0
        self.p2_score = 0

    def update(self, elapsed : float, events : list):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.p1 -= elapsed / 1000.0 * 100
        if keys[pygame.K_s]:
            self.p1 += elapsed / 1000.0 * 100
        if keys[pygame.K_UP]:
            self.p2 -= elapsed / 1000.0 * 100
        if keys[pygame.K_DOWN]:
            self.p2 += elapsed / 1000.0 * 100

        self.ball += self.vel * elapsed / 1000.0
        
        #if ball collides with paddle
        if self.ball.x <= self.paddle_width and self.p1 - self.paddle_height / 2 + self.ball_size / 2 <= self.ball.y <= self.p1 + self.paddle_height / 2 - self.ball_size / 2:
            self.vel.x *= -1
            self.vel.y += (self.ball.y - self.p1) / 32

        if self.ball.x >= 512 - self.paddle_width and self.p2 - self.paddle_height / 2 + self.ball_size / 2 <= self.ball.y <= self.p2 + self.paddle_height / 2 - self.ball_size / 2:
            self.vel.x *= -1
            self.vel.y += (self.ball.y - self.p2) / 32

        #if ball collides with top or bottom
        if self.ball.y <= self.ball_size / 2 or self.ball.y >= 512 - self.ball_size / 2:
            self.vel.y *= -1
        
        #if ball goes off screen
        if self.ball.x <= 0:
            self.p2_score += 1
            self.ball = pygame.Vector2(self.paddle_width, 256)
            angle = random.uniform(-math.pi / 4, math.pi / 4)
            velocity = 64
            self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * velocity
            self.p1 = 256
            self.p2 = 256

        if self.ball.x >= 512:
            self.p1_score += 1
            self.ball = pygame.Vector2(self.paddle_width, 256)
            angle = random.uniform(-math.pi / 4, math.pi / 4)
            velocity = 64
            self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * velocity
            self.p1 = 256
            self.p2 = 256



    def render(self, screen : pygame.Surface):

        # Draw ball
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.ball.x - self.ball_size / 2, self.ball.y - self.ball_size / 2, self.ball_size, self.ball_size))

        # Draw paddles
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, self.p1 - self.paddle_height / 2, self.paddle_width, self.paddle_height))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen.get_width() - self.paddle_width, self.p2 - self.paddle_height / 2, self.paddle_width, self.paddle_height))
    
        # Draw score
        font = pygame.font.SysFont("Arial", 32)
        screen.blit(font.render(str(self.p1_score), True, (255, 255, 255)), (screen.get_width() / 4, 0))
        screen.blit(font.render(str(self.p2_score), True, (255, 255, 255)), (screen.get_width() * 3 / 4, 0))