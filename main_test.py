import pygame
import sys

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "Anime Style Game Art"

BACKGROUND = (30, 30, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROOM_FILL = (70, 80, 110)
FLOOR_FILL = (55, 60, 85)


def draw_room(screen):
    # Back wall
    wall_rect = pygame.Rect(250, 120, 500, 250)
    pygame.draw.rect(screen, ROOM_FILL, wall_rect)
    pygame.draw.rect(screen, WHITE, wall_rect, 2)

    # Floor as a trapezoid to fake perspective
    floor_points = [(180, 520), (820, 520), (700, 370), (300, 370)]
    pygame.draw.polygon(screen, FLOOR_FILL, floor_points)
    pygame.draw.polygon(screen, WHITE, floor_points, 2)

    # Simple room corner lines
    pygame.draw.line(screen, WHITE, (250, 370), (180, 520), 2)
    pygame.draw.line(screen, WHITE, (750, 370), (820, 520), 2)

    # A simple object in the room
    obj_rect = pygame.Rect(460, 300, 80, 70)
    pygame.draw.rect(screen, (120, 140, 190), obj_rect)
    pygame.draw.rect(screen, WHITE, obj_rect, 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    print("Room test launched")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)
        draw_room(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()