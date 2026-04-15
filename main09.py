import pygame
import sys

WIDTH = 1000
HEIGHT = 700
FPS = 60
TITLE = "Room + Door + Chest + Ruby"

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

DOOR_FILL = (120, 155, 155)
DOOR_SHADOW = (80, 105, 105)

POSTER_FILL = (145, 120, 170)
POSTER_SHADOW = (100, 80, 120)

BOX_FILL = (160, 120, 120)
BOX_SHADOW = (110, 80, 80)

PLANT_FILL = (120, 160, 145)
PLANT_SHADOW = (80, 110, 95)

CHEST_FILL = (165, 115, 70)
CHEST_SHADOW = (110, 75, 45)
CHEST_BAND = (220, 190, 80)

RUBY_FILL = (220, 40, 60)
RUBY_SHADOW = (150, 20, 35)

HUD_BG = (20, 22, 30)
HUD_SLOT = (70, 76, 95)
HUD_SLOT_SHADOW = (50, 54, 70)

FONT_COLOR = (240, 240, 245)


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

    if len(points) == 4:
        shadow_points = [
            (points[0][0] + 40, points[0][1] - 10),
            (points[1][0] - 40, points[1][1] - 10),
            points[2],
            points[3],
        ]
        pygame.draw.polygon(screen, shadow_color, shadow_points)

    pygame.draw.polygon(screen, outline_color, points, 2)


def draw_ruby(screen, center_x, center_y, scale=1):
    points = [
        (center_x, center_y - 12 * scale),
        (center_x + 10 * scale, center_y - 2 * scale),
        (center_x + 6 * scale, center_y + 10 * scale),
        (center_x, center_y + 15 * scale),
        (center_x - 6 * scale, center_y + 10 * scale),
        (center_x - 10 * scale, center_y - 2 * scale),
    ]
    pygame.draw.polygon(screen, RUBY_FILL, points)
    pygame.draw.polygon(screen, RUBY_SHADOW, [points[0], points[1], points[2], points[3]])
    pygame.draw.polygon(screen, WHITE, points, 2)


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
    def hitbox(self):
        r = self.rect
        return pygame.Rect(r.x + 4, r.y + 8, r.w - 8, r.h - 10)

    @property
    def feet_y(self):
        return int(self.y + self.height // 2 + 2)

    def move(self, keys, colliders, bounds):
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed

        if dx != 0:
            self.x += dx
            if self.collides_with_any(colliders):
                self.x -= dx

        if dy != 0:
            self.y += dy
            if self.collides_with_any(colliders):
                self.y -= dy

        self.x = max(bounds["min_x"], min(bounds["max_x"], self.x))
        self.y = max(bounds["min_y"], min(bounds["max_y"], self.y))

    def collides_with_any(self, colliders):
        for collider in colliders:
            if self.hitbox.colliderect(collider):
                return True
        return False

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
    def __init__(self, x, y, w, h, base_color, shadow_color, kind="prop", solid=True, sort_offset=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = base_color
        self.shadow_color = shadow_color
        self.kind = kind
        self.solid = solid
        self.sort_offset = sort_offset

    @property
    def sort_y(self):
        return self.rect.bottom + self.sort_offset

    @property
    def collider(self):
        return pygame.Rect(
            self.rect.x + 4,
            self.rect.y + 10,
            self.rect.w - 8,
            self.rect.h - 10
        )

    def draw_shadow(self, screen):
        shadow_width = self.rect.width
        shadow_surface = pygame.Surface((shadow_width, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 70), (0, 0, shadow_width, 14))
        screen.blit(shadow_surface, (self.rect.x, self.rect.bottom - 6))

    def draw(self, screen):
        draw_anime_rect(screen, self.rect, self.base_color, self.shadow_color)


class Door(Prop):
    def __init__(self, x, y, w=80, h=150):
        super().__init__(x, y, w, h, DOOR_FILL, DOOR_SHADOW, kind="door", solid=False, sort_offset=2)

    @property
    def interact_rect(self):
        base = pygame.Rect(self.rect.x + 8, self.rect.y + 20, self.rect.w - 16, self.rect.h - 20)
        return base.inflate(20, 20)

    def draw(self, screen):
        draw_anime_rect(screen, self.rect, self.base_color, self.shadow_color)
        handle = pygame.Rect(self.rect.right - 16, self.rect.centery - 5, 6, 10)
        pygame.draw.rect(screen, WHITE, handle)
        pygame.draw.rect(screen, BLACK, handle, 1)


class Chest:
    def __init__(self, x, y):
        self.base_rect = pygame.Rect(x, y, 86, 52)
        self.is_open = False
        self.loot_taken = False

    @property
    def sort_y(self):
        return self.base_rect.bottom

    @property
    def collider(self):
        return pygame.Rect(
            self.base_rect.x + 4,
            self.base_rect.y + 12,
            self.base_rect.w - 8,
            self.base_rect.h - 10
        )

    @property
    def interact_rect(self):
        return self.collider.inflate(24, 20)

    def draw_shadow(self, screen):
        shadow_surface = pygame.Surface((self.base_rect.width, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), (0, 0, self.base_rect.width, 16))
        screen.blit(shadow_surface, (self.base_rect.x, self.base_rect.bottom - 6))

    def draw(self, screen):
        base = pygame.Rect(self.base_rect.x, self.base_rect.y + 18, self.base_rect.w, 34)
        lid_closed = pygame.Rect(self.base_rect.x, self.base_rect.y, self.base_rect.w, 24)

        if not self.is_open:
            draw_anime_rect(screen, base, CHEST_FILL, CHEST_SHADOW)
            draw_anime_rect(screen, lid_closed, CHEST_FILL, CHEST_SHADOW)

            band = pygame.Rect(self.base_rect.centerx - 6, self.base_rect.y + 6, 12, 40)
            pygame.draw.rect(screen, CHEST_BAND, band)
            pygame.draw.rect(screen, BLACK, band, 2)
        else:
            draw_anime_rect(screen, base, CHEST_FILL, CHEST_SHADOW)

            lid_points = [
                (self.base_rect.x + 6, self.base_rect.y + 18),
                (self.base_rect.x + self.base_rect.w - 8, self.base_rect.y + 8),
                (self.base_rect.x + self.base_rect.w - 18, self.base_rect.y - 14),
                (self.base_rect.x + 10, self.base_rect.y - 4),
            ]
            draw_anime_polygon(screen, lid_points, CHEST_FILL, CHEST_SHADOW)

            band = pygame.Rect(self.base_rect.centerx - 6, self.base_rect.y + 20, 12, 26)
            pygame.draw.rect(screen, CHEST_BAND, band)
            pygame.draw.rect(screen, BLACK, band, 2)


class Backpack:
    def __init__(self, cols=2, rows=3):
        self.cols = cols
        self.rows = rows
        self.items = []

    def add_item(self, item_name):
        capacity = self.cols * self.rows
        if len(self.items) < capacity:
            self.items.append(item_name)
            return True
        return False

    def draw(self, screen, font):
        panel_rect = pygame.Rect(18, HEIGHT - 180, 180, 150)
        pygame.draw.rect(screen, HUD_BG, panel_rect)
        pygame.draw.rect(screen, WHITE, panel_rect, 2)

        label = font.render("Backpack", True, FONT_COLOR)
        screen.blit(label, (panel_rect.x + 12, panel_rect.y + 10))

        slot_size = 42
        pad_x = 16
        pad_y = 38
        gap = 10

        for row in range(self.rows):
            for col in range(self.cols):
                slot_x = panel_rect.x + pad_x + col * (slot_size + gap)
                slot_y = panel_rect.y + pad_y + row * (slot_size + gap)
                slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)

                pygame.draw.rect(screen, HUD_SLOT, slot_rect)
                inner_shadow = pygame.Rect(slot_x + 12, slot_y + 12, slot_size - 12, slot_size - 12)
                pygame.draw.rect(screen, HUD_SLOT_SHADOW, inner_shadow)
                pygame.draw.rect(screen, WHITE, slot_rect, 2)

                idx = row * self.cols + col
                if idx < len(self.items):
                    item = self.items[idx]
                    if item == "ruby":
                        draw_ruby(screen, slot_rect.centerx, slot_rect.centery, scale=1)


class Room:
    def __init__(self, room_id, bounds):
        self.room_id = room_id
        self.bounds = bounds
        self.floor_points = [(180, 520), (820, 520), (700, 370), (300, 370)]
        self.wall_rect = pygame.Rect(250, 120, 500, 250)

        self.wall_decor = []
        self.floor_objects = []
        self.interactives = []

    def colliders(self):
        colliders = []
        for obj in self.floor_objects:
            if hasattr(obj, "solid") and obj.solid:
                colliders.append(obj.collider)
            elif isinstance(obj, Chest):
                colliders.append(obj.collider)
        return colliders

    def draw_base(self, screen, room_fill, room_shadow, floor_fill, floor_shadow):
        draw_anime_rect(screen, self.wall_rect, room_fill, room_shadow)
        draw_anime_polygon(screen, self.floor_points, floor_fill, floor_shadow)
        pygame.draw.line(screen, WHITE, (250, 370), (180, 520), 2)
        pygame.draw.line(screen, WHITE, (750, 370), (820, 520), 2)

    def draw_all(self, screen, player):
        drawables = []

        for obj in self.floor_objects:
            drawables.append(("obj", obj.sort_y, obj))

        drawables.append(("player_shadow", player.feet_y - 1, player))
        drawables.append(("player", player.feet_y, player))
        drawables.sort(key=lambda item: item[1])

        for kind, _, obj in drawables:
            if kind == "obj":
                if hasattr(obj, "draw_shadow"):
                    obj.draw_shadow(screen)
                obj.draw(screen)
            elif kind == "player_shadow":
                obj.draw_shadow(screen)
            elif kind == "player":
                obj.draw(screen)


def create_room_1():
    room = Room(
        room_id=1,
        bounds={"min_x": 220, "max_x": 780, "min_y": 260, "max_y": 500}
    )

    poster = Prop(320, 170, 90, 120, POSTER_FILL, POSTER_SHADOW, solid=False, kind="poster")
    room.wall_decor.append(poster)

    table = Prop(460, 300, 80, 70, OBJECT_FILL, OBJECT_SHADOW)
    box = Prop(610, 330, 60, 40, BOX_FILL, BOX_SHADOW)
    plant = Prop(360, 390, 70, 55, PLANT_FILL, PLANT_SHADOW)

    door = Door(660, 220, 70, 150)

    room.floor_objects.extend([table, box, plant, door])
    room.interactives.append(door)

    return room


def create_room_2():
    room = Room(
        room_id=2,
        bounds={"min_x": 220, "max_x": 780, "min_y": 260, "max_y": 500}
    )

    banner = Prop(315, 165, 120, 100, (120, 130, 175), (85, 90, 125), solid=False, kind="banner")
    room.wall_decor.append(banner)

    chest = Chest(475, 360)
    crate = Prop(610, 370, 70, 55, BOX_FILL, BOX_SHADOW)
    stand = Prop(330, 340, 60, 85, OBJECT_FILL, OBJECT_SHADOW)

    room.floor_objects.extend([stand, crate, chest])
    room.interactives.append(chest)

    return room


def draw_room_1(screen, room, player):
    room.draw_base(screen, ROOM_FILL, ROOM_SHADOW, FLOOR_FILL, FLOOR_SHADOW)

    for decor in room.wall_decor:
        decor.draw(screen)

    room.draw_all(screen, player)


def draw_room_2(screen, room, player):
    room_fill = (82, 96, 138)
    room_shadow = (55, 66, 96)
    floor_fill = (70, 58, 78)
    floor_shadow = (48, 38, 56)

    room.draw_base(screen, room_fill, room_shadow, floor_fill, floor_shadow)

    for decor in room.wall_decor:
        decor.draw(screen)

    shrine = pygame.Rect(560, 180, 100, 110)
    draw_anime_rect(screen, shrine, (130, 95, 145), (90, 65, 100))

    room.draw_all(screen, player)


def draw_prompt(screen, font, text):
    text_surf = font.render(text, True, FONT_COLOR)
    padding_x = 12
    padding_y = 8
    bg_rect = pygame.Rect(
        WIDTH // 2 - text_surf.get_width() // 2 - padding_x,
        HEIGHT - 42 - text_surf.get_height(),
        text_surf.get_width() + padding_x * 2,
        text_surf.get_height() + padding_y * 2
    )
    pygame.draw.rect(screen, HUD_BG, bg_rect)
    pygame.draw.rect(screen, WHITE, bg_rect, 2)
    screen.blit(text_surf, (bg_rect.x + padding_x, bg_rect.y + padding_y))


def find_interaction(player, room):
    for obj in room.interactives:
        if player.hitbox.colliderect(obj.interact_rect):
            return obj
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 20)

    player = Player(500, 430)
    backpack = Backpack()

    rooms = {
        1: create_room_1(),
        2: create_room_2(),
    }
    current_room_id = 1

    running = True
    while running:
        e_pressed_this_frame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    e_pressed_this_frame = True

        keys = pygame.key.get_pressed()
        current_room = rooms[current_room_id]

        player.move(keys, current_room.colliders(), current_room.bounds)

        interaction_obj = find_interaction(player, current_room)

        if e_pressed_this_frame and interaction_obj is not None:
            if isinstance(interaction_obj, Door) and current_room_id == 1:
                current_room_id = 2
                player.x = 280
                player.y = 430
                current_room = rooms[current_room_id]

            elif isinstance(interaction_obj, Chest) and current_room_id == 2:
                if not interaction_obj.is_open:
                    interaction_obj.is_open = True

                    if not interaction_obj.loot_taken:
                        added = backpack.add_item("ruby")
                        if added:
                            interaction_obj.loot_taken = True

        screen.fill(BACKGROUND)

        if current_room_id == 1:
            draw_room_1(screen, rooms[1], player)
        elif current_room_id == 2:
            draw_room_2(screen, rooms[2], player)

        backpack.draw(screen, font)

        prompt_text = None
        interaction_obj = find_interaction(player, rooms[current_room_id])

        if isinstance(interaction_obj, Door):
            prompt_text = "Press E to enter the next room"
        elif isinstance(interaction_obj, Chest):
            if not interaction_obj.is_open:
                prompt_text = "Press E to open the chest"
            elif interaction_obj.loot_taken:
                prompt_text = "The chest is empty"

        if prompt_text:
            draw_prompt(screen, font, prompt_text)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()