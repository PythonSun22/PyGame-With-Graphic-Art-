import pygame

pygame.init()

# ----------------------------
# Setup
# ----------------------------
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Palette")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
LIGHT_GRAY = (230, 230, 230)
BLUE = (80, 140, 255)
RED = (220, 80, 80)


class InputBox:
    def __init__(self, x, y, w, h, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.label = label

    def handle_mouse_click(self, mouse_pos):
        """
        Returns:
            clicked_this_box (bool): True if this box was clicked
        """
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            return True
        return False

    def deactivate_and_clear(self):
        """
        Called when user clicks away from this box.
        Clears unfinished input.
        """
        self.active = False
        self.text = ""

    def handle_keydown(self, event):
        if not self.active:
            return None

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        elif event.key == pygame.K_RETURN:
            try:
                entered_text = int(self.text)
                print(f"{self.label} entered:", entered_text)
                self.text = ""
                return entered_text
            except ValueError:
                print("Invalid input, must be integer.")
                self.text = ""   

        else:
            # Add typed character
            # event.unicode gives the actual typed character
            if event.unicode.isprintable():
                self.text += event.unicode

        return None

    def draw(self, surface, font):
        # Label above box
        label_surf = font.render(self.label, True, BLACK)
        surface.blit(label_surf, (self.rect.x, self.rect.y - 30))

        # Box fill
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect)

        # Border color depends on active state
        border_color = BLUE if self.active else GRAY
        pygame.draw.rect(surface, border_color, self.rect, 3)

        # Text
        text_surf = font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))


# ----------------------------
# Create 3 boxes
# ----------------------------
boxes = [
    InputBox(100, 100, 250, 50, "Red Channel"),
    InputBox(100, 200, 250, 50, "Green Channel"),
    InputBox(100, 300, 250, 50, "Blue Channel")
]
red_box = pygame.Rect(400, 100, 50, 50)
blue_box = pygame.Rect(400, 200, 50, 50)
green_box = pygame.Rect(400, 300, 50, 50)
combo_box = pygame.Rect(500, 100, 100, 250)
r = 255
g = 255
b = 255


running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                clicked_box = None

                # Find which box was clicked
                for box in boxes:
                    if box.handle_mouse_click(event.pos):
                        clicked_box = box

                        break

                # If a box was clicked, deactivate/clear all others
                if clicked_box is not None:
                    for box in boxes:
                        if box is not clicked_box:
                            box.deactivate_and_clear()
                else:
                    # Clicked outside all boxes -> clear all active boxes
                    for box in boxes:
                        if box.active:
                            box.deactivate_and_clear()

        elif event.type == pygame.KEYDOWN:
            for box in boxes:
                result = box.handle_keydown(event)
                if result is not None:
                    if clicked_box.rect.y == 100:
                        r = result
                    if clicked_box.rect.y == 200:
                        b = result
                    if clicked_box.rect.y == 300:
                        g = result
                    print("Submitted:", result)
                    #Logic for which var to assign it to r,b,g

    for box in boxes:
        box.draw(screen, font)

    instructions = font.render(
        "Click a box to enter the color channel value [0-255], then hit enter.",
        True,
        BLACK
    )
    screen.blit(instructions, (40, 30))

    #Draw Colored Rectangles
    pygame.draw.rect(screen, (r,b,g), combo_box)
    pygame.draw.rect(screen, (r, 0, 0), red_box)
    pygame.draw.rect(screen, (0, b, 0), blue_box)
    pygame.draw.rect(screen, (0, 0, g), green_box)                 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()