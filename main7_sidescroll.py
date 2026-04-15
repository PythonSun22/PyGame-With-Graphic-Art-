import sys
import random
import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "main03 - Side Scrolling Hallway"

# Colors
BACKGROUND = (20, 22, 32)
WHITE = (245, 245, 255)
BLACK = (0, 0, 0)

CEILING_FILL = (78, 88, 128)
CEILING_SHADOW = (55, 62, 92)

FLOOR_FILL = (58, 66, 92)
FLOOR_SHADOW = (38, 44, 64)

BACK_WALL_FILL = (98, 108, 150)
BACK_WALL_SHADOW = (72, 80, 116)

LOWER_WALL_FILL = (84, 92, 128)
LOWER_WALL_SHADOW = (62, 68, 96)

PANEL_FILL = (145, 125, 172)
PANEL_SHADOW = (100, 82, 122)

DOOR_FILL = (122, 152, 158)
DOOR_SHADOW = (88, 112, 118)

PIPE_FILL = (118, 182, 150)
PIPE_SHADOW = (82, 126, 102)

LIGHT_FILL = (255, 236, 176)
LIGHT_SHADOW = (220, 196, 126)

COLUMN_FILL = (150, 138, 170)
COLUMN_SHADOW = (102, 92, 118)

PLAYER_FILL = (220, 225, 255)
PLAYER_SHADOW = (150, 160, 200)

SEGMENT_WIDTH = 220
ACTIVE_MARGIN = 3


def draw_shaded_rect(screen, rect, base_color, shadow_color, outline_color=WHITE):
    pygame.draw.rect(screen, base_color, rect)
    shadow_rect = pygame.Rect(
        rect.x + rect.w // 3,
        rect.y + rect.h // 3,
        rect.w - rect.w // 3,
        rect.h - rect.h // 3,
    )
    pygame.draw.rect(screen, shadow_color, shadow_rect)
    pygame.draw.rect(screen, outline_color, rect, 2)


def draw_shaded_polygon(screen, points, base_color, shadow_color, outline_color=WHITE):
    pygame.draw.polygon(screen, base_color, points)

    if len(points) == 4:
        shadow_points = [
            (points[0][0], points[0][1]),
            (points[1][0], points[1][1]),
            (
                points[2][0] - (points[2][0] - points[3][0]) // 2,
                points[2][1] - (points[2][1] - points[3][1]) // 2,
            ),
            (
                points[3][0] + (points[2][0] - points[3][0]) // 2,
                points[3][1] + (points[0][1] - points[3][1]) // 2,
            ),
        ]
        pygame.draw.polygon(screen, shadow_color, shadow_points)

    pygame.draw.polygon(screen, outline_color, points, 2)


class Player:
    def __init__(self, x, floor_y):
        self.x = x
        self.y = floor_y
        self.width = 26
        self.height = 42
        self.speed = 5
        self.walk_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height),
            self.width,
            self.height,
        )

    def update(self, keys):
        moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            moving = True

        self.x = max(120, min(WIDTH - 120, self.x))

        if moving:
            self.walk_timer += 0.18

    def draw_shadow(self, screen):
        shadow = pygame.Surface((42, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 90), (0, 0, 42, 14))
        screen.blit(shadow, (int(self.x - 21), int(self.y - 6)))

    def draw(self, screen):
        bob = int(abs((self.walk_timer % 1.0) - 0.5) * 4)
        body_rect = pygame.Rect(self.rect.x, self.rect.y - bob, self.rect.w, self.rect.h)

        pygame.draw.rect(screen, PLAYER_FILL, body_rect)

        shadow_rect = pygame.Rect(
            body_rect.x + body_rect.w // 3,
            body_rect.y + body_rect.h // 3,
            body_rect.w - body_rect.w // 3,
            body_rect.h - body_rect.h // 3,
        )
        pygame.draw.rect(screen, PLAYER_SHADOW, shadow_rect)
        pygame.draw.rect(screen, WHITE, body_rect, 2)

        head_center = (int(self.x), int(body_rect.y - 10))
        pygame.draw.circle(screen, PLAYER_FILL, head_center, 10)
        pygame.draw.circle(screen, WHITE, head_center, 10, 2)

        pygame.draw.line(
            screen,
            WHITE,
            (head_center[0] - 3, head_center[1] + 2),
            (head_center[0] + 3, head_center[1] + 2),
            1,
        )


class HallwaySegment:
    def __init__(self, index, floor_y, ceiling_y):
        self.index = index
        self.world_x = index * SEGMENT_WIDTH
        self.floor_y = floor_y
        self.ceiling_y = ceiling_y

        rng = random.Random(index * 9173 + 71)

        self.feature = rng.choice(["panel", "door", "pipe", "column", None, None])
        self.has_light = rng.choice([True, False, True])
        self.has_floor_line = rng.choice([True, False])
        self.wall_split_offset = rng.randint(-6, 8)

    def draw(self, screen, camera_x):
        sx = self.world_x - camera_x

        if sx > WIDTH + SEGMENT_WIDTH or sx < -SEGMENT_WIDTH:
            return

        x = int(sx)
        w = SEGMENT_WIDTH

        floor_front_y = self.floor_y
        floor_back_y = self.floor_y - 70

        ceiling_front_y = self.ceiling_y
        ceiling_back_y = self.ceiling_y + 55

        left = x
        right = x + w

        # Ceiling
        ceiling_poly = [
            (left, ceiling_front_y),
            (right, ceiling_front_y),
            (right - 28, ceiling_back_y),
            (left + 28, ceiling_back_y),
        ]
        draw_shaded_polygon(screen, ceiling_poly, CEILING_FILL, CEILING_SHADOW)

        # Floor
        floor_poly = [
            (left, floor_front_y),
            (right, floor_front_y),
            (right - 28, floor_back_y),
            (left + 28, floor_back_y),
        ]
        draw_shaded_polygon(screen, floor_poly, FLOOR_FILL, FLOOR_SHADOW)

        # Back wall
        wall_rect = pygame.Rect(left + 28, ceiling_back_y, w - 56, floor_back_y - ceiling_back_y)
        draw_shaded_rect(screen, wall_rect, BACK_WALL_FILL, BACK_WALL_SHADOW)

        # Lower wall trim band
        lower_band = pygame.Rect(left + 28, floor_back_y - 65 + self.wall_split_offset, w - 56, 38)
        draw_shaded_rect(screen, lower_band, LOWER_WALL_FILL, LOWER_WALL_SHADOW)

        # Side seam lines
        pygame.draw.line(screen, WHITE, (left, floor_front_y), (left + 28, floor_back_y), 2)
        pygame.draw.line(screen, WHITE, (right, floor_front_y), (right - 28, floor_back_y), 2)
        pygame.draw.line(screen, WHITE, (left, ceiling_front_y), (left + 28, ceiling_back_y), 2)
        pygame.draw.line(screen, WHITE, (right, ceiling_front_y), (right - 28, ceiling_back_y), 2)

        # Vertical segment seams
        pygame.draw.line(screen, WHITE, (left + 28, ceiling_back_y), (left + 28, floor_back_y), 1)
        pygame.draw.line(screen, WHITE, (right - 28, ceiling_back_y), (right - 28, floor_back_y), 1)

        if self.has_floor_line:
            pygame.draw.line(
                screen,
                WHITE,
                (left + 20, floor_front_y - 20),
                (right - 20, floor_front_y - 20),
                2
            )

        if self.has_light:
            self.draw_light(screen, left, right, ceiling_front_y, ceiling_back_y)

        if self.feature:
            self.draw_feature(screen, wall_rect)

    def draw_light(self, screen, left, right, ceiling_front_y, ceiling_back_y):
        light_w = 56
        light_h = 18
        cx = (left + right) // 2

        top_rect = pygame.Rect(cx - light_w // 2, ceiling_front_y + 16, light_w, light_h)
        draw_shaded_rect(screen, top_rect, LIGHT_FILL, LIGHT_SHADOW)

        glow = pygame.Surface((90, 36), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 240, 180, 65), (0, 0, 90, 36))
        screen.blit(glow, (cx - 45, ceiling_front_y + 12))

    def draw_feature(self, screen, wall_rect):
        if self.feature == "panel":
            rect = pygame.Rect(wall_rect.x + 22, wall_rect.y + 26, wall_rect.w - 44, 86)
            draw_shaded_rect(screen, rect, PANEL_FILL, PANEL_SHADOW)

        elif self.feature == "door":
            rect = pygame.Rect(wall_rect.x + 28, wall_rect.y + 18, wall_rect.w - 56, wall_rect.h - 30)
            draw_shaded_rect(screen, rect, DOOR_FILL, DOOR_SHADOW)

            handle = pygame.Rect(rect.right - 16, rect.centery - 6, 6, 12)
            pygame.draw.rect(screen, WHITE, handle)
            pygame.draw.rect(screen, BLACK, handle, 1)

        elif self.feature == "pipe":
            pipe_x = wall_rect.centerx - 10
            pipe_rect = pygame.Rect(pipe_x, wall_rect.y + 10, 20, wall_rect.h - 20)
            draw_shaded_rect(screen, pipe_rect, PIPE_FILL, PIPE_SHADOW)

            band1 = pygame.Rect(pipe_rect.x - 6, pipe_rect.y + 16, 32, 10)
            band2 = pygame.Rect(pipe_rect.x - 6, pipe_rect.bottom - 26, 32, 10)
            draw_shaded_rect(screen, band1, PIPE_FILL, PIPE_SHADOW)
            draw_shaded_rect(screen, band2, PIPE_FILL, PIPE_SHADOW)

        elif self.feature == "column":
            rect = pygame.Rect(wall_rect.x + 12, wall_rect.y, 30, wall_rect.h)
            draw_shaded_rect(screen, rect, COLUMN_FILL, COLUMN_SHADOW)


class InfiniteHallway:
    def __init__(self):
        self.camera_x = 0.0
        self.scroll_speed = 3.0

        self.floor_y = HEIGHT - 80
        self.ceiling_y = 80

        self.segments = {}

    def update(self):
        self.camera_x += self.scroll_speed

        current_index = int(self.camera_x // SEGMENT_WIDTH)

        needed = range(current_index - ACTIVE_MARGIN, current_index + (WIDTH // SEGMENT_WIDTH) + ACTIVE_MARGIN + 2)
        new_segments = {}

        for i in needed:
            if i in self.segments:
                new_segments[i] = self.segments[i]
            else:
                new_segments[i] = HallwaySegment(i, self.floor_y, self.ceiling_y)

        self.segments = new_segments

    def draw(self, screen):
        screen.fill(BACKGROUND)

        # Far background strip
        far_rect = pygame.Rect(0, self.ceiling_y + 55, WIDTH, self.floor_y - self.ceiling_y - 125)
        pygame.draw.rect(screen, (42, 48, 72), far_rect)

        for seg in sorted(self.segments.values(), key=lambda s: s.index):
            seg.draw(screen, self.camera_x)


def draw_hud(screen, hallway):
    font = pygame.font.SysFont("consolas", 22)
    text = font.render(f"camera_x: {int(hallway.camera_x)}", True, WHITE)
    screen.blit(text, (20, 20))

    font2 = pygame.font.SysFont("consolas", 18)
    text2 = font2.render("A/D or Left/Right to move character sideways", True, WHITE)
    screen.blit(text2, (20, 48))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    hallway = InfiniteHallway()
    player = Player(220, hallway.floor_y)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player.update(keys)
        hallway.update()

        hallway.draw(screen)
        player.draw_shadow(screen)
        player.draw(screen)
        draw_hud(screen, hallway)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()