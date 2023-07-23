import pygame

from snake import Snake
from tetris import Tetris
from pong import Pong

# Main entry point
def main():

    # initialize pygame
    pygame.init()
    pygame.display.set_caption("pygames | menu")

    # global variables
    global screen, clock, running, game, menu, menu_index, paused, interval

    # initialize global variables
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    running = True
    game = None
    menu = [ Snake(), Tetris(), Pong() ]
    menu_index = 0
    paused = False
    interval = 60

    # main loop
    while running:
        
        update(interval)
        render()

        clock.tick(interval)

    # quit pygame when loop is exited
    pygame.quit()

def update(elapsed : float):
    global running, game, menu, menu_index, paused, events

    # First handle menu events and common in-game events
    events = pygame.event.get()
    for event in events:
        
        # Standard quit event
        if event.type == pygame.QUIT:
            running = False
            break

        # Handle events for menu (when not in game - game is None)
        if game is None:

            # On key down
            if event.type == pygame.KEYDOWN:

                # Quit game from menu
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                # Menu up/down navigation
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    menu_index = (menu_index - 1) % len(menu)
                
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    menu_index = (menu_index + 1) % len(menu)

                # Launch game
                elif event.key == pygame.K_RETURN:
                    game = menu[menu_index]
                    pygame.display.set_caption("pygames | " + game.name)
                    game.start()

        # Handle common in-game events (when in game - game is not None)
        else:

            # On key down
            if event.type == pygame.KEYDOWN:
                
                # Quit game to menu
                if event.key == pygame.K_ESCAPE:
                    game.quit()
                    paused = False
                    game = None
                    pygame.display.set_caption("pygames | menu")

                # Toggle pause game
                elif event.key == pygame.K_SPACE:
                    paused = not paused

    # Finally, update current game
    if game is not None and not paused:
        game.update(elapsed, pygame.event.get())

def render():
    global game, menu, screen, menu_index
    
    # Clear screen
    screen.fill((0, 0, 0))

    # Render menu
    if game is None:
    
        # Some constants
        leading = 128   # leading space from top of screen
        w = 256         # width of menu item box
        h = 48          # height of menu item box

        # For each menu item
        for i in range(len(menu)):

            # Draw menu item text centered
            text = pygame.font.Font(None, 36).render(menu[i].name, True, (255, 255, 255))
            textpos = text.get_rect(centerx=screen.get_width()/2, centery=leading + i * h)
            screen.blit(text, textpos)

            # Draw a box around the selected menu item
            if i == menu_index:
                pygame.draw.rect(screen, (255, 255, 255), (screen.get_width()/2 - w/2, leading + i * h - h/2, w, h), 1)

    
    # Render current game
    else:
        game.render(screen)

    if paused:
        # Draw a semi-transparent black rectangle over the screen
        s = pygame.Surface(screen.get_size())
        s.set_alpha(192)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        # Draw "PAUSED" text
        text = pygame.font.Font(None, 36).render("PAUSED", True, (255, 255, 255))
        textpos = text.get_rect(centerx=screen.get_width()/2, centery=screen.get_height()/2)
        screen.blit(text, textpos)

    # Flip buffers
    pygame.display.flip()

if __name__ == "__main__":
    main()