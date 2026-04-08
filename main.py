import pygame
import sys

from settings import WIDTH, HEIGHT, FPS, TITLE
from colors import BACKGROUND, WHITE

def draw_test_scene(screen):
    #Outline circle
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 60, 2)
    #Simple floor line (hinting at space)
    pygame.draw.line(screen, WHITE, (200,500), (800, 500), 2)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    #Game Loop
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        screen.fill(BACKGROUND)
        draw_test_scene(screen)

        # Draw
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "main":
    main()