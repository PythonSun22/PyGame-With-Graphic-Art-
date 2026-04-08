import pygame
import sys

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "Anime Style Game Art"

BACKGROUND = (30, 30, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROOM_FILL = (95, 105, 145)
ROOM_SHADOW = (65, 72, 100)

FLOOR_FILL = (60, 68, 95)
FLOOR_SHADOW = (42, 48, 70)

OBJECT_FILL = (125, 145, 195)
OBJECT_SHADOW = (85, 100, 145)


def draw_anime_rect(screen, rect, base_color, shadow_color, outline_color=WHITE):
    # Base fill
    pygame.draw.rect(screen, base_color, rect)

    # Hard shadow band on lower-right portion
    shadow_rect = pygame.Rect(
        rect.x + rect.w // 3,
        rect.y + rect.h // 3,
        rect.w - rect.w // 3,
        rect.h - rect.h // 3,
    )
    pygame.draw.rect(screen, shadow_color, shadow_rect)

    # Outline
    pygame.draw.rect(screen, outline_color, rect, 2)


def draw_anime_polygon(screen, points, base_color, shadow_color, outline_color=WHITE):
    # Base fill
    pygame.draw.polygon(screen, base_color, points)

    # Very simple shadow band:
    # darken the lower portion by drawing another polygon inside it
    shadow_points = [
        (
            points[0][0] + 40,
            points[0][1] - 10,
        ),
        (
            points[1][0] - 40,
            points[1][1] - 10,
        ),
        points[2],
        points[3],
    ]
    pygame.draw.polygon(screen, shadow_color, shadow_points)

    # Outline
    pygame.draw.polygon(screen, outline_color, points, 2)


def create_light_surface(radius, alpha_max=180):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for r in range(radius, 0, -2):
        alpha = int(alpha_max * (r / radius))
        color = (0, 0, 0, alpha)
        pygame.draw.circle(surface, color, (radius, radius), r)

    return surface


def draw_room(screen, mouse_pos, light):
    # Back wall
    wall_rect = pygame.Rect(250, 120, 500, 250)
    draw_anime_rect(screen, wall_rect, ROOM_FILL, ROOM_SHADOW)

    # Floor trapezoid
    floor_points = [(180, 520), (820, 520), (700, 370), (300, 370)]
    draw_anime_polygon(screen, floor_points, FLOOR_FILL, FLOOR_SHADOW)

    # Corner lines
    pygame.draw.line(screen, WHITE, (250, 370), (180, 520), 2)
    pygame.draw.line(screen, WHITE, (750, 370), (820, 520), 2)

    # Center object
    obj_rect = pygame.Rect(460, 300, 80, 70)
    draw_anime_rect(screen, obj_rect, OBJECT_FILL, OBJECT_SHADOW)

    # Small "poster" on wall for style
    poster = pygame.Rect(320, 170, 90, 120)
    draw_anime_rect(screen, poster, (145, 120, 170), (100, 80, 120))

    # Another object
    box_rect = pygame.Rect(610, 330, 60, 40)
    draw_anime_rect(screen, box_rect, (160, 120, 120), (110, 80, 80))

    # Darkness overlay
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 120))

    # Light cutout follows mouse
    darkness.blit(
        light,
        (mouse_pos[0] - 180, mouse_pos[1] - 180),
        special_flags=pygame.BLEND_RGBA_SUB,
    )

    # Apply darkness
    screen.blit(darkness, (0, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    light = create_light_surface(180, 140)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BACKGROUND)
        draw_room(screen, mouse_pos, light)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()