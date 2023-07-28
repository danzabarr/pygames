import pygame
import random
from game import Game

class Invaders(Game):

    def __init__(self):
        super().__init__("invaders")

    def start(self):
        self.score = 0
        self.player = Player(256 - 16, 512 - 32, 32, 32)
        self.invaders = []
        self.projectiles = []

        for i in range(8):
            for j in range(4):
                self.invaders.append(Invader(64 + i * 36, 64 + j * 36, (255, 255, 255)))

    
    def update(self, elapsed : float, events : list):
        
        # Handle controls
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= 256 * elapsed / 1000.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += 256 * elapsed / 1000.0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.projectiles.append(self.player.shoot((255, 255, 255)))

        # Update game objects
        for projectile in self.projectiles:
            projectile.move(elapsed)
    
        for invader in self.invaders:
            invader.move(elapsed)

        # Randomly shoot projectiles
        if random.random() < 0.01:
            self.projectiles.append(self.invaders[random.randint(0, len(self.invaders) - 1)].shoot((255, 255, 255)))

        # Remove projectiles that go off screen
        for projectile in self.projectiles:
            if projectile.y < 0 or projectile.y > 512:
                self.projectiles.remove(projectile)

        # If an invader reaches the bottom, restart the game
        for invader in self.invaders:
            if invader.y > 512 - 16:
                self.start()
                return
            
        # If a projectile hits an entity, remove the entity and the projectile
        for projectile in self.projectiles:

            if projectile.faction == "player":
                for invader in self.invaders:
                    if invader.collides(projectile):
                        self.invaders.remove(invader)
                        self.projectiles.remove(projectile)
                        self.score += 1
                        break

            elif projectile.faction == "invader":
                if self.player.collides(projectile):
                    self.start()
                    return
                
        # If all invaders are dead, spawn a new wave
        if len(self.invaders) == 0:
            for i in range(8):
                for j in range(4):
                    self.invaders.append(Invader(64 + i * 36, 64 + j * 36, (255, 255, 255)))

    def render(self, screen : pygame.Surface):

        # Draw player
        self.player.draw(screen)
        
        # Draw invaders
        for invader in self.invaders:
            invader.draw(screen)

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

        # Draw score
        screen.blit(pygame.font.SysFont("Arial", 24).render(str(self.score), True, (255, 255, 255)), (0, 0))

class Entity:

    def __init__(self, faction, x, y, w, h, color):
        self.faction = faction
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))

    def shoot(self, color):
        
        x = self.x + self.w / 2
        y = self.y - 4 if self.faction == "player" else self.y + self.h + 4
        vx = 0
        vy = -50 if self.faction == "player" else 50

        return Projectile(self.faction, x, y, vx, vy, color)

    def collides(self, other):
        return self.x < other.x + other.w and self.x + self.w > other.x and self.y < other.y + other.h and self.y + self.h > other.y

class Invader(Entity):

    def __init__(self, x, y, color):
        super().__init__("invader", x, y, 16, 16, color)
        self.direction = 1
        self.move_counter = 0

    def move(self, elapsed):
        self.move_counter += elapsed / 1000.0
        if self.move_counter >= 1:
            self.move_counter -= 1
            self.x += self.direction * 16
            if self.x <= 0 or self.x >= 512 - 16:
                self.direction *= -1
                self.y += 16

class Player(Entity):

    def __init__(self, x, y, w, h):
        super().__init__("player", x, y, w, h, (255, 255, 255))

class Projectile(Entity):

    def __init__(self, faction, x, y, vx, vy, color):
        super().__init__(faction, x, y, 4, 12, color)
        self.vx = vx
        self.vy = vy

    def move(self, elapsed):
        self.x += self.vx * elapsed / 1000.0
        self.y += self.vy * elapsed / 1000.0