import sys
import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "main02 - Retro Character Shape Study"

# Colors
SKY = (120, 190, 255)
GROUND_TOP = (210, 170, 90)
GROUND_SIDE = (160, 110, 60)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (210, 40, 40)
DARK_RED = (150, 25, 25)

BLUE = (60, 90, 220)
DARK_BLUE = (40, 60, 150)

BROWN = (120, 75, 40)
DARK_BROWN = (80, 50, 25)

SKIN = (255, 215, 170)
DARK_SKIN = (220, 180, 140)

GREEN = (40, 180, 70)
DARK_GREEN = (20, 120, 45)

YELLOW = (245, 210, 60)
DARK_YELLOW = (190, 155, 35)


def draw_outlined_rect(screen, color, outline, rect, width=2):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, outline, rect, width)


def draw_outlined_circle(screen, color, outline, center, radius, width=2):
    pygame.draw.circle(screen, color, center, radius)
    pygame.draw.circle(screen, outline, center, radius, width)


def draw_ground(screen):
    top_rect = pygame.Rect(0, 560, WIDTH, 140)
    side_rect = pygame.Rect(0, 590, WIDTH, 110)

    pygame.draw.rect(screen, GROUND_TOP, top_rect)
    pygame.draw.rect(screen, GROUND_SIDE, side_rect)

    pygame.draw.line(screen, BLACK, (0, 590), (WIDTH, 590), 2)

    # Simple decorative marks
    for x in range(0, WIDTH, 70):
        pygame.draw.line(screen, DARK_BROWN, (x, 620), (x + 20, 640), 2)
        pygame.draw.line(screen, DARK_BROWN, (x + 25, 650), (x + 45, 670), 2)


def draw_pipe(screen, x, y, w=90, h=120):
    body_rect = pygame.Rect(x, y, w, h)
    lip_rect = pygame.Rect(x - 10, y - 22, w + 20, 28)

    pygame.draw.rect(screen, GREEN, body_rect)
    pygame.draw.rect(screen, DARK_GREEN, (x + w // 2, y, w // 2, h))
    pygame.draw.rect(screen, BLACK, body_rect, 2)

    pygame.draw.rect(screen, GREEN, lip_rect)
    pygame.draw.rect(screen, DARK_GREEN, (lip_rect.x + lip_rect.w // 2, lip_rect.y, lip_rect.w // 2, lip_rect.h))
    pygame.draw.rect(screen, BLACK, lip_rect, 2)

    # Vertical highlight lines
    pygame.draw.line(screen, WHITE, (x + 12, y + 8), (x + 12, y + h - 8), 2)
    pygame.draw.line(screen, DARK_GREEN, (x + w - 12, y + 8), (x + w - 12, y + h - 8), 2)


def draw_mystery_box(screen, x, y, size=60):
    box = pygame.Rect(x, y, size, size)
    inner = pygame.Rect(x + 6, y + 6, size - 12, size - 12)

    pygame.draw.rect(screen, YELLOW, box)
    pygame.draw.rect(screen, BLACK, box, 2)

    pygame.draw.rect(screen, DARK_YELLOW, inner, 3)

    # Corner bolts
    bolt_size = 6
    bolts = [
        (x + 8, y + 8),
        (x + size - 14, y + 8),
        (x + 8, y + size - 14),
        (x + size - 14, y + size - 14),
    ]
    for bx, by in bolts:
        pygame.draw.rect(screen, DARK_YELLOW, (bx, by, bolt_size, bolt_size))
        pygame.draw.rect(screen, BLACK, (bx, by, bolt_size, bolt_size), 1)

    # Simple question-mark style symbol
    pygame.draw.circle(screen, BROWN, (x + size // 2, y + 20), 8)
    pygame.draw.rect(screen, BROWN, (x + size // 2 - 4, y + 20, 8, 14))
    pygame.draw.circle(screen, BROWN, (x + size // 2, y + 42), 4)

    pygame.draw.circle(screen, BLACK, (x + size // 2, y + 20), 8, 2)
    pygame.draw.rect(screen, BLACK, (x + size // 2 - 4, y + 20, 8, 14), 2)
    pygame.draw.circle(screen, BLACK, (x + size // 2, y + 42), 4, 2)


class RetroPlumber:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_shadow(self, screen):
        shadow = pygame.Surface((56, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80), (0, 0, 56, 18))
        screen.blit(shadow, (self.x - 28, self.y + 44))

    def draw(self, screen):
        x = self.x
        y = self.y

        # Legs
        left_leg = pygame.Rect(x - 18, y + 20, 14, 24)
        right_leg = pygame.Rect(x + 4, y + 20, 14, 24)
        draw_outlined_rect(screen, BLUE, BLACK, left_leg)
        draw_outlined_rect(screen, BLUE, BLACK, right_leg)

        # Shoes
        left_shoe = pygame.Rect(x - 22, y + 40, 20, 10)
        right_shoe = pygame.Rect(x + 2, y + 40, 20, 10)
        draw_outlined_rect(screen, BROWN, BLACK, left_shoe)
        draw_outlined_rect(screen, BROWN, BLACK, right_shoe)

        # Shirt / torso base
        torso = pygame.Rect(x - 22, y - 4, 44, 28)
        draw_outlined_rect(screen, RED, BLACK, torso)

        # Arms
        left_arm = pygame.Rect(x - 30, y + 2, 10, 22)
        right_arm = pygame.Rect(x + 20, y + 2, 10, 22)
        draw_outlined_rect(screen, RED, BLACK, left_arm)
        draw_outlined_rect(screen, RED, BLACK, right_arm)

        # Gloves
        left_glove = pygame.Rect(x - 32, y + 18, 12, 10)
        right_glove = pygame.Rect(x + 20, y + 18, 12, 10)
        draw_outlined_rect(screen, WHITE, BLACK, left_glove)
        draw_outlined_rect(screen, WHITE, BLACK, right_glove)

        # Overalls
        overall_body = pygame.Rect(x - 18, y + 4, 36, 24)
        draw_outlined_rect(screen, BLUE, BLACK, overall_body)

        # Overall straps
        left_strap = pygame.Rect(x - 14, y - 2, 8, 16)
        right_strap = pygame.Rect(x + 6, y - 2, 8, 16)
        draw_outlined_rect(screen, BLUE, BLACK, left_strap)
        draw_outlined_rect(screen, BLUE, BLACK, right_strap)

        # Buttons
        pygame.draw.circle(screen, YELLOW, (x - 10, y + 10), 3)
        pygame.draw.circle(screen, YELLOW, (x + 10, y + 10), 3)
        pygame.draw.circle(screen, BLACK, (x - 10, y + 10), 3, 1)
        pygame.draw.circle(screen, BLACK, (x + 10, y + 10), 3, 1)

        # Head
        head_center = (x, y - 20)
        draw_outlined_circle(screen, SKIN, BLACK, head_center, 18)

        # Ears
        pygame.draw.circle(screen, SKIN, (x - 18, y - 20), 4)
        pygame.draw.circle(screen, SKIN, (x + 18, y - 20), 4)
        pygame.draw.circle(screen, BLACK, (x - 18, y - 20), 4, 1)
        pygame.draw.circle(screen, BLACK, (x + 18, y - 20), 4, 1)

        # Nose
        pygame.draw.ellipse(screen, DARK_SKIN, (x - 3, y - 20, 10, 8))
        pygame.draw.ellipse(screen, BLACK, (x - 3, y - 20, 10, 8), 1)

        # Mustache
        moustache = [
            (x - 12, y - 12),
            (x + 12, y - 12),
            (x + 8, y - 4),
            (x - 8, y - 4),
        ]
        pygame.draw.polygon(screen, DARK_BROWN, moustache)
        pygame.draw.polygon(screen, BLACK, moustache, 2)

        # Eyes
        pygame.draw.ellipse(screen, BLACK, (x - 8, y - 28, 4, 10))
        pygame.draw.ellipse(screen, BLACK, (x + 4, y - 28, 4, 10))

        # Hair sideburns
        pygame.draw.rect(screen, BROWN, (x - 18, y - 28, 5, 14))
        pygame.draw.rect(screen, BROWN, (x + 13, y - 28, 5, 14))
        pygame.draw.rect(screen, BLACK, (x - 18, y - 28, 5, 14), 1)
        pygame.draw.rect(screen, BLACK, (x + 13, y - 28, 5, 14), 1)

        # Hat brim
        brim = pygame.Rect(x - 22, y - 38, 44, 8)
        draw_outlined_rect(screen, RED, BLACK, brim)

        # Hat dome
        pygame.draw.ellipse(screen, RED, (x - 20, y - 54, 40, 24))
        pygame.draw.ellipse(screen, BLACK, (x - 20, y - 54, 40, 24), 2)

        # Hat logo circle
        pygame.draw.circle(screen, WHITE, (x, y - 42), 7)
        pygame.draw.circle(screen, BLACK, (x, y - 42), 7, 1)

        # Tiny emblem hint
        pygame.draw.line(screen, RED, (x - 2, y - 45), (x - 2, y - 39), 2)
        pygame.draw.line(screen, RED, (x + 2, y - 45), (x + 2, y - 39), 2)
        pygame.draw.line(screen, RED, (x - 2, y - 45), (x + 2, y - 42), 2)
        pygame.draw.line(screen, RED, (x - 2, y - 39), (x + 2, y - 42), 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    player = RetroPlumber(220, 500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SKY)

        draw_ground(screen)

        # Static scene pieces
        draw_pipe(screen, 540, 440, 90, 120)
        draw_pipe(screen, 720, 400, 105, 160)
        draw_mystery_box(screen, 410, 360, 60)

        player.draw_shadow(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()