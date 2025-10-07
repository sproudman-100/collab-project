
import pygame

from tree import Tree
from player import Player
from enemy import Enemy

import random

# Define grid size
GRID_X = 18
GRID_Y = 32

def main():

    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("PyZelda")
    screen = pygame.display.set_mode((GRID_Y * 50, GRID_X * 50))
    running = True
    clock = pygame.time.Clock()

    # Set the dimensions of each grid cell
    grid_width = screen.get_width() // GRID_Y
    grid_height = screen.get_height() // GRID_X

    # Create player instance
    player = Player(GRID_X, GRID_Y, grid_width, grid_height)
    
    # Create enemy instance
    enemy = Enemy(GRID_X, GRID_Y, grid_width, grid_height)

    # Create multiple tree instances
    trees = []
    tree_positions = [(random.randint(0, GRID_Y-1), random.randint(0, GRID_X-1)) for _ in range(30)]

    for x, y in tree_positions:
        # Make sure tree fits within grid bounds
        if x + 2 <= GRID_Y and y + 3 <= GRID_X:
            trees.append(Tree(x, y, grid_width, grid_height))

    # Pass collidable objects to player and enemy
    player.set_collidable_objects(trees)
    enemy.set_collidable_objects(trees)

    # Main game loop
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        # Draw background
        screen.fill("green")
        # for x in range(GRID_Y + 1):
        #     pygame.draw.line(screen, (0, 0, 0), (x * grid_width, 0), (x * grid_width, screen.get_height()), 1)
        # for y in range(GRID_X + 1):
        #     pygame.draw.line(screen, (0, 0, 0), (0, y * grid_height), (screen.get_width(), y * grid_height), 1)

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
        
        # Update enemy
        enemy.update(dt)
        
        # Draw all entities sorted by y position (top to bottom)
        all_entities = [player] + [enemy] + trees
        sorted_entities = sorted(all_entities, key=lambda entity: entity.y)
        
        for entity in sorted_entities:
            entity.draw(screen)

        # Update display
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()