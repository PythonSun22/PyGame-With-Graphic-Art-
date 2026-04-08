import pygame
import sys

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "Anime Line Game"

BACKGROUND = (30, 30, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROOM_FILL = (95, 105, 145)
ROOM_SHADOW = (65, 72, 100)

FLOOR_FILL = (60, 68, 95)
FLOOR_SHADOW = (42, 48, 70)

OBJECT_FILL = (125, 145, 195)
OBJECT_SHADOW = (85, 100, 145)

PLAYER_FILL = (210, 220, 255)
PLAYER_SHADOW = (140, 150, 190)
PLAYER_SPEED = 4


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 26
        self.height = 42
        self.speed = PLAYER_SPEED

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    @property
    def feet_y(self):
        return int(self.y + self.height // 2 + 2)

    def move(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(220, min(780, self.x))
        self.y = max(260, min(500, self.y))

    def draw_shadow(self, screen):
        shadow_surface = pygame.Surface((40, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 90), (0, 0, 40, 16))
        screen.blit(shadow_surface, (int(self.x - 20), int(self.feet_y - 6)))

    def draw(self, screen):
        body_rect = self.rect

        pygame.draw.rect(screen, PLAYER_FILL, body_rect)

        shadow_rect = pygame.Rect(
            body_rect.x + body_rect.w // 3,
            body_rect.y + body_rect.h // 3,
            body_rect.w - body_rect.w // 3,
            body_rect.h - body_rect.h // 3,
        )
        pygame.draw.rect(screen, PLAYER_SHADOW, shadow_rect)

        pygame.draw.rect(screen, WHITE, body_rect, 2)

        head_center = (int(self.x), int(self.y - self.height // 2 - 10))
        pygame.draw.circle(screen, PLAYER_FILL, head_center, 10)
        pygame.draw.circle(screen, WHITE, head_center, 10, 2)

        pygame.draw.line(
            screen,
            WHITE,
            (head_center[0] - 3, head_center[1] + 2),
            (head_center[0] + 3, head_center[1] + 2),
            1
        )

        pygame.draw.line(
            screen,
            WHITE,
            (body_rect.x + 4, body_rect.bottom + 2),
            (body_rect.right - 4, body_rect.bottom + 2),
            2
        )


class Prop:
    def __init__(self, x, y, w, h, base_color, shadow_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = base_color
        self.shadow_color = shadow_color

    @property
    def sort_y(self):
        return self.rect.bottom

    def draw_shadow(self, screen):
        shadow_width = self.rect.width
        shadow_surface = pygame.Surface((shadow_width, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(
            shadow_surface,
            (0, 0, 0, 70),
            (0, 0, shadow_width, 14)
        )
        screen.blit(shadow_surface, (self.rect.x, self.rect.bottom - 6))

    def draw(self, screen):
        draw_anime_rect(screen, self.rect, self.base_color, self.shadow_color)


def draw_anime_rect(screen, rect, base_color, shadow_color, outline_color=WHITE):
    pygame.draw.rect(screen, base_color, rect)

    shadow_rect = pygame.Rect(
        rect.x + rect.w // 3,
        rect.y + rect.h // 3,
        rect.w - rect.w // 3,
        rect.h - rect.h // 3,
    )
    pygame.draw.rect(screen, shadow_color, shadow_rect)

    pygame.draw.rect(screen, outline_color, rect, 2)


def draw_anime_polygon(screen, points, base_color, shadow_color, outline_color=WHITE):
    pygame.draw.polygon(screen, base_color, points)

    shadow_points = [
        (points[0][0] + 40, points[0][1] - 10),
        (points[1][0] - 40, points[1][1] - 10),
        points[2],
        points[3],
    ]
    pygame.draw.polygon(screen, shadow_color, shadow_points)

    pygame.draw.polygon(screen, outline_color, points, 2)


def create_light_surface(radius, alpha_max=180):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    for r in range(radius, 0, -2):
        alpha = int(alpha_max * (r / radius))
        pygame.draw.circle(surface, (0, 0, 0, alpha), (radius, radius), r)

    return surface


def draw_room(screen):
    wall_rect = pygame.Rect(250, 120, 500, 250)
    draw_anime_rect(screen, wall_rect, ROOM_FILL, ROOM_SHADOW)

    floor_points = [(180, 520), (820, 520), (700, 370), (300, 370)]
    draw_anime_polygon(screen, floor_points, FLOOR_FILL, FLOOR_SHADOW)

    pygame.draw.line(screen, WHITE, (250, 370), (180, 520), 2)
    pygame.draw.line(screen, WHITE, (750, 370), (820, 520), 2)


def draw_lighting(screen, mouse_pos, light):
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 120))

    darkness.blit(
        light,
        (mouse_pos[0] - 180, mouse_pos[1] - 180),
        special_flags=pygame.BLEND_RGBA_SUB,
    )

    screen.blit(darkness, (0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    light = create_light_surface(180, 140)
    player = Player(500, 430)

    props = [
        Prop(460, 300, 80, 70, OBJECT_FILL, OBJECT_SHADOW),
        Prop(610, 330, 60, 40, (160, 120, 120), (110, 80, 80)),
        Prop(360, 390, 70, 55, (120, 160, 145), (80, 110, 95)),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        player.move(keys)

        screen.fill(BACKGROUND)
        draw_room(screen)

        # Draw poster separately because it belongs on the wall, not the floor
        poster_rect = pygame.Rect(320, 170, 90, 120)
        draw_anime_rect(screen, poster_rect, (145, 120, 170), (100, 80, 120))

        drawables = []

        for prop in props:
            drawables.append(("prop", prop.sort_y, prop))

        drawables.append(("player_shadow", player.feet_y - 1, player))
        drawables.append(("player", player.feet_y, player))

        drawables.sort(key=lambda item: item[1])

        for kind, _, obj in drawables:
            if kind == "prop":
                obj.draw_shadow(screen)
                obj.draw(screen)
            elif kind == "player_shadow":
                obj.draw_shadow(screen)
            elif kind == "player":
                obj.draw(screen)

        draw_lighting(screen, mouse_pos, light)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()