import pygame
import sys
from constants import *

pygame.init()
screen = pygame.display.set_mode((540, 500))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 18)
pygame.display.set_caption("Color Palette")

class InputBox:
    def __init__(self,x,y,w,h,label=""):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = ""
        self.active = False
        self.label = label

    def handle_mouse_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.active = True
        return False
    
    def deactivate_and_clear(self):
        self.ative = False
        self.text = ""

    def handle_keydown(self, event):
        if not self.active:
            return None
        
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        elif event.key == pygame.K_RETURN:
            entered_text = self.text
            print(f"{self.label} entered:", entered_text)
            self.text = ""
            ###
            return entered_text
        
        return None
    def draw(self, surface, font):
        label_surf = font.render(self.label, True, BLACK)
        surface.blit(label_surf, (self.rect.x, self.rect.y - 30))

        pygame.draw.rect(surface, LIGHT_GRAY, self.rect)

        border_color = BLUE if self.active else LIGHT_GRAY
        pygame.draw.rect(surface, border_color, self.rect, 3)

        text_surf = font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))


def main():
    #Create 3 Input Boxes
    boxes = [
        InputBox(100, 20, 100, 30, "Red Channel"),
        InputBox(220, 20, 100, 30, "Green Channel"),
        InputBox(340, 20, 100, 30, "Blue Channel")
    ]
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
                if event.button == 1: #Left click
                    clicked_box = None
                    for box in boxes:
                        if box.handle_mouse_click(event.pos):
                            clicked_box = box
                            break
                    if clicked_box is not None:
                        for box in boxes:
                            if box is not clicked_box:
                                box.deactivate_and_clear()
                    else:
                        for mox in boxes:
                            if box.active:
                                box.deactivate_and_clear()

            elif event.type == pygame.KEYDOWN:
                for box in boxes:
                    result = box.handle_keydown(event)
                    if result is not None:
                        print("Submitted::", result)

        for box in boxes:
            box.draw(screen, font)

        instructions = font.render(
            "Click a box to enter the color channel value [0-255], then hit enter.",
            True, BLACK
        )
        screen.blit(instructions, (40, 30))

        pygame.display.flip()
        clock.tick(60)

    

if __name__ == "__main__":
    main()
