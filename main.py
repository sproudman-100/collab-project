
import pygame

from player import Player

# Define grid size
GRID_X = 18
GRID_Y = 32

def main():

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((GRID_Y * 50, GRID_X * 50))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Set the dimensions of each grid cell
    grid_width = screen.get_width() // GRID_Y
    grid_height = screen.get_height() // GRID_X

    # Create player instance
    player = Player(GRID_X, GRID_Y, grid_width, grid_height)

    # Main game loop
    while running:
        
        # Draw background
        screen.fill("green")
        for x in range(GRID_Y + 1):
            pygame.draw.line(screen, (0, 0, 0), (x * grid_width, 0), (x * grid_width, screen.get_height()), 1)
        for y in range(GRID_X + 1):
            pygame.draw.line(screen, (0, 0, 0), (0, y * grid_height), (screen.get_width(), y * grid_height), 1)

        # Handle user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    player.move(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.move(0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.move(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.move(1, 0)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_w):
                    player.stop('up')
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.stop('down')
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    player.stop('left')
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.stop('right')

        # Update and draw player
        player.update()
        player.draw(screen)

        # Update display
        pygame.display.flip()
        #dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == '__main__':
    main()