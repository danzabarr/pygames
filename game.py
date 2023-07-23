import pygame

# Base class for all games

class Game():

    # Called at the start of the program.
    def __init__(self, name):
        self.name = name

    # Called when game is started, override this with your own start code
    def start(self):
        pass

    # Called every frame, override this with your own update code
    def update(self, elapsed : float, events : list):
        pass

    # Called every frame, override this with your own render code
    def render(self, screen : pygame.Surface):
        screen.blit(pygame.font.SysFont("Arial", 24).render(self.name, True, (255, 255, 255)), (0, 0))
