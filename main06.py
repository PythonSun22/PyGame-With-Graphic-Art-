import sys
import random
import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "main03 - Infinite Corridor"

# Colors
BACKGROUND = (18, 20, 30)
WHITE = (245, 245, 255)
BLACK = (0, 0, 0)

CEILING_FILL = (72, 82, 120)
CEILING_SHADOW = (50, 58, 88)

FLOOR_FILL = (58, 66, 92)
FLOOR_SHADOW = (38, 44, 64)

LEFT_WALL_FILL = (92, 102, 145)
LEFT_WALL_SHADOW = (66, 74, 108)

RIGHT_WALL_FILL = (102, 112, 155)
RIGHT_WALL_SHADOW = (76, 84, 116)

PANEL_FILL = (140, 120, 170)
PANEL_SHADOW = (95, 80, 120)

DOOR_FILL = (120, 150, 155)
DOOR_SHADOW = (85, 110, 115)

LIGHT_FILL = (255, 235, 170)
LIGHT_GLOW = (255, 235, 170, 70)

PIPE_FILL = (120, 180, 150)
PIPE_SHADOW = (80, 125, 100)

COLUMN_FILL = (145, 135, 165)
COLUMN_SHADOW = (98, 90, 115)

PLAYER_FILL = (220, 225, 255)
PLAYER_SHADOW = (150, 160, 200)

SEGMENT_LENGTH = 220
VISIBLE_SEGMENTS = 10


def clamp(value, low, high):
    return max(low, min(high, value))


def lerp(a, b, t):
    return a + (b - a) * t


def draw_shaded_polygon(screen, points, base_color, shadow_color, outline_color=WHITE):
    pygame.draw.polygon(screen, base_color, points)
    if len(points) == 4:
        # crude shadow band on lower-right side
        shadow_points = [
            (
                int(lerp(points[0][0], points[3][0], 0.30)),
                int(lerp(points[0][1], points[3][1], 0.30)),
            ),
            (
                int(lerp(points[1][0], points[2][0], 0.30)),
                int(lerp(points[1][1], points[2][1], 0.30)),
            ),
            points[2],
            points[3],
        ]
        pygame.draw.polygon(screen, shadow_color, shadow_points)
    pygame.draw.polygon(screen, outline_color, points, 2)


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


class Player:
    def __init__(self):
        self.x = WIDTH * 0.25
        self.y = 0
        self.width = 24
        self.height = 42
        self.speed = 6
        self.walk_phase = 0.0

    def update(self, keys):
        moving = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            moving = True

        self.x = clamp(self.x, 120, WIDTH - 120)

        if moving:
            self.walk_phase += 0.16

    def draw_shadow(self, screen):
        shadow = pygame.Surface((46, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 95), (0, 0, 46, 16))
        screen.blit(shadow, (int(self.x - 23), int(self.y + 28)))

    def draw(self, screen):
        bob = int(2 * abs((self.walk_phase % 1.0) - 0.5))
        body_rect = pygame.Rect(int(self.x - 12), int(self.y - 18 - bob), self.width, self.height)

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


class CorridorSegment:
    def __init__(self, index):
        self.index = index
        self.world_x = index * SEGMENT_LENGTH
        self.seed = index * 977 + 1337

        rng = random.Random(self.seed)
        self.left_feature = rng.choice(["panel", "door", "pipe", "column", None])
        self.right_feature = rng.choice(["panel", "door", "pipe", "column", None])
        self.light_style = rng.choice(["single", "double", "none"])
        self.floor_marks = rng.choice([True, False])
        self.panel_offset = rng.randint(-8, 10)

    def screen_x(self, camera_x):
        return self.world_x - camera_x

    def draw(self, screen, camera_x, floor_y, vanishing_y):
        sx = self.screen_x(camera_x)

        if sx > WIDTH + SEGMENT_LENGTH or sx < -SEGMENT_LENGTH * 2:
            return

        x0 = sx
        x1 = sx + SEGMENT_LENGTH

        # Corridor bounds
        near_left = 90
        near_right = WIDTH - 90
        near_top = 85
        floor_top = floor_y

        # Far corridor slice for this segment
        t0 = clamp((x0 + 200) / (WIDTH + 500), 0.0, 1.0)
        t1 = clamp((x1 + 200) / (WIDTH + 500), 0.0, 1.0)

        # These create the fake narrowing toward the distance
        left0 = int(lerp(near_left, WIDTH * 0.45, t0))
        right0 = int(lerp(near_right, WIDTH * 0.55, t0))
        top0 = int(lerp(near_top, vanishing_y - 10, t0))
        bottom0 = int(lerp(floor_top, vanishing_y + 25, t0))

        left1 = int(lerp(near_left, WIDTH * 0.45, t1))
        right1 = int(lerp(near_right, WIDTH * 0.55, t1))
        top1 = int(lerp(near_top, vanishing_y - 10, t1))
        bottom1 = int(lerp(floor_top, vanishing_y + 25, t1))

        # Ceiling strip
        ceiling = [(left0, top0), (right0, top0), (right1, top1), (left1, top1)]
        draw_shaded_polygon(screen, ceiling, CEILING_FILL, CEILING_SHADOW)

        # Floor strip
        floor = [(left0, bottom0), (right0, bottom0), (right1, bottom1), (left1, bottom1)]
        draw_shaded_polygon(screen, floor, FLOOR_FILL, FLOOR_SHADOW)

        # Left wall strip
        left_wall = [(0, top0), (left0, top0), (left1, top1), (0, top1)]
        draw_shaded_polygon(screen, left_wall, LEFT_WALL_FILL, LEFT_WALL_SHADOW)

        # Right wall strip
        right_wall = [(right0, top0), (WIDTH, top0), (WIDTH, top1), (right1, top1)]
        draw_shaded_polygon(screen, right_wall, RIGHT_WALL_FILL, RIGHT_WALL_SHADOW)

        # Corridor seam lines
        pygame.draw.line(screen, WHITE, (left0, top0), (left1, top1), 2)
        pygame.draw.line(screen, WHITE, (right0, top0), (right1, top1), 2)
        pygame.draw.line(screen, WHITE, (left0, bottom0), (left1, bottom1), 2)
        pygame.draw.line(screen, WHITE, (right0, bottom0), (right1, bottom1), 2)

        # Vertical slice line
        pygame.draw.line(screen, WHITE, (left0, top0), (left0, bottom0), 1)
        pygame.draw.line(screen, WHITE, (right0, top0), (right0, bottom0), 1)

        # Ceiling light
        self.draw_ceiling_light(screen, x0, x1, top0, top1, left0, right0, left1, right1)

        # Left wall feature
        if self.left_feature:
            self.draw_wall_feature(
                screen,
                side="left",
                feature=self.left_feature,
                top0=top0,
                bottom0=bottom0,
                top1=top1,
                bottom1=bottom1,
                left0=left0,
                left1=left1,
            )

        # Right wall feature
        if self.right_feature:
            self.draw_wall_feature(
                screen,
                side="right",
                feature=self.right_feature,
                top0=top0,
                bottom0=bottom0,
                top1=top1,
                bottom1=bottom1,
                right0=right0,
                right1=right1,
            )

        # Floor center marks
        if self.floor_marks:
            midx0 = (left0 + right0) // 2
            midx1 = (left1 + right1) // 2
            pygame.draw.line(screen, WHITE, (midx0, bottom0 - 8), (midx1, bottom1 - 8), 2)

    def draw_ceiling_light(self, screen, x0, x1, top0, top1, left0, right0, left1, right1):
        if self.light_style == "none":
            return

        center0 = (left0 + right0) // 2
        center1 = (left1 + right1) // 2
        y0 = top0 + 16
        y1 = top1 + 16

        if self.light_style == "single":
            poly = [
                (center0 - 18, y0),
                (center0 + 18, y0),
                (center1 + 12, y1),
                (center1 - 12, y1),
            ]
            draw_shaded_polygon(screen, poly, LIGHT_FILL, (220, 190, 120))
        else:
            poly1 = [
                (center0 - 40, y0),
                (center0 - 8, y0),
                (center1 - 6, y1),
                (center1 - 28, y1),
            ]
            poly2 = [
                (center0 + 8, y0),
                (center0 + 40, y0),
                (center1 + 28, y1),
                (center1 + 6, y1),
            ]
            draw_shaded_polygon(screen, poly1, LIGHT_FILL, (220, 190, 120))
            draw_shaded_polygon(screen, poly2, LIGHT_FILL, (220, 190, 120))

    def draw_wall_feature(self, screen, side, feature, top0, bottom0, top1, bottom1, left0=None, left1=None, right0=None, right1=None):
        wall_mid_y0 = int(lerp(top0, bottom0, 0.52))
        wall_mid_y1 = int(lerp(top1, bottom1, 0.52))

        feat_top0 = wall_mid_y0 - 38 + self.panel_offset
        feat_bot0 = wall_mid_y0 + 32 + self.panel_offset
        feat_top1 = wall_mid_y1 - 26 + self.panel_offset
        feat_bot1 = wall_mid_y1 + 22 + self.panel_offset

        if side == "left":
            outer0 = left0 - 12
            inner0 = left0 - 70
            outer1 = left1 - 8
            inner1 = left1 - 48
        else:
            outer0 = right0 + 12
            inner0 = right0 + 70
            outer1 = right1 + 8
            inner1 = right1 + 48

        poly = [(outer0, feat_top0), (inner0, feat_top0), (inner1, feat_top1), (outer1, feat_top1)]
        poly2 = [(outer0, feat_bot0), (inner0, feat_bot0), (inner1, feat_bot1), (outer1, feat_bot1)]

        if feature == "panel":
            body = [(outer0, feat_top0), (inner0, feat_top0), (inner1, feat_bot1), (outer1, feat_bot0)]
            draw_shaded_polygon(screen, body, PANEL_FILL, PANEL_SHADOW)

        elif feature == "door":
            body = [(outer0, feat_top0 - 18), (inner0, feat_top0 - 18), (inner1, feat_bot1 + 16), (outer1, feat_bot0 + 16)]
            draw_shaded_polygon(screen, body, DOOR_FILL, DOOR_SHADOW)

            # handle/light
            cx0 = int(lerp(outer0, inner0, 0.78 if side == "left" else 0.22))
            cy0 = int(lerp(feat_top0, feat_bot0, 0.55))
            cx1 = int(lerp(outer1, inner1, 0.78 if side == "left" else 0.22))
            cy1 = int(lerp(feat_top1, feat_bot1, 0.55))
            pygame.draw.line(screen, WHITE, (cx0, cy0), (cx1, cy1), 3)

        elif feature == "pipe":
            body = [(outer0, feat_top0), (inner0, feat_top0), (inner1, feat_bot1), (outer1, feat_bot0)]
            draw_shaded_polygon(screen, body, PIPE_FILL, PIPE_SHADOW)
            # interior pipe stripes
            pygame.draw.line(screen, WHITE, (outer0, feat_top0 + 16), (outer1, feat_top1 + 12), 2)
            pygame.draw.line(screen, WHITE, (outer0, feat_bot0 - 16), (outer1, feat_bot1 - 12), 2)

        elif feature == "column":
            body = [(outer0, top0), (inner0, top0), (inner1, bottom1), (outer1, bottom0)]
            draw_shaded_polygon(screen, body, COLUMN_FILL, COLUMN_SHADOW)


class InfiniteCorridor:
    def __init__(self):
        self.camera_x = 0.0
        self.speed = 4.0
        self.floor_y = HEIGHT - 105
        self.vanishing_y = 265

        self.segments = {}
        for i in range(-2, VISIBLE_SEGMENTS + 3):
            self.segments[i] = CorridorSegment(i)

    def update(self, player_dx):
        # Corridor scroll speed comes from "forward motion"
        self.camera_x += self.speed + player_dx * 0.65

        current_index = int(self.camera_x // SEGMENT_LENGTH)

        needed = range(current_index - 2, current_index + VISIBLE_SEGMENTS + 3)
        new_segments = {}
        for i in needed:
            if i in self.segments:
                new_segments[i] = self.segments[i]
            else:
                new_segments[i] = CorridorSegment(i)
        self.segments = new_segments

    def draw(self, screen):
        # far background haze
        pygame.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, HEIGHT))
        pygame.draw.line(screen, WHITE, (0, self.vanishing_y), (WIDTH, self.vanishing_y), 1)

        ordered = sorted(self.segments.values(), key=lambda seg: seg.index, reverse=True)
        for seg in ordered:
            seg.draw(screen, self.camera_x, self.floor_y, self.vanishing_y)


def draw_hud(screen, camera_x):
    font = pygame.font.SysFont("consolas", 22)
    text = font.render(f"camera_x: {int(camera_x)}", True, WHITE)
    screen.blit(text, (20, 20))

    small = pygame.font.SysFont("consolas", 18)
    info = small.render("A/D or Left/Right to shift pace", True, WHITE)
    screen.blit(info, (20, 48))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    corridor = InfiniteCorridor()
    player = Player()
    player.y = corridor.floor_y - 18

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        old_x = player.x
        player.update(keys)
        player_dx = player.x - old_x

        corridor.update(player_dx)

        corridor.draw(screen)
        player.draw_shadow(screen)
        player.draw(screen)
        draw_hud(screen, corridor.camera_x)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()