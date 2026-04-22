import pygame
from pygame.locals import *
import sys
from constants import *

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 18)



# GENERATOR FUNCTIONS
def create_rectangle(left, top, width, height, color):
    new_rect = pygame.rect((left,top), (width, height))
    return new_rect


#GAME LOOP: COLOR PALETTE
def main():
    
    user_text = ""
    question_r = "Red? [0-255]: "
    r = 255 
    g = 255 
    b = 255

    running = True
    while running:

        #Iterates through event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        r = int(user_text)
                        print("User entered: ", user_text)
                        user_text = ""
                    except ValueError:
                        print("Invalid input")
                    #throw more errors for out of range and limit input to 3 characters.
                    #isdigit() filter
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else: 
                    user_text += event.unicode
            #elif event.type == pygame.MOUSEBUTTONDOWN:
                #mousebutton_down_this_frame = True
                #mouse_pos = pygame.get_pos()
            #elif event.type == pygame.MOUSEBUTTONUP:
                #mousebutton_up_this_frame = True
                #mouse_pos = pygame.get_pos()
            #elif event.type == pygame.MOUSEWHEEL:
                #scrolling_this_frame = True
                #mouse_pos = pygame.get_pos()
                #print("mouse pos: " + mouse_pos)
                #print(event)
                #print(event.x, event.y)
                #print(event.which)
        #Background
        screen.fill(BLACK)
       
        
        #Draw Rectangles
        red_band = pygame.Rect(100, 100, 100, 100)
        pygame.draw.rect(screen, (r, 0, 0), red_band)
        green_band = pygame.Rect(220, 100, 100, 100)
        pygame.draw.rect(screen, (0, g, 0), green_band)
        blue_band = pygame.Rect(340, 100, 100, 100)
        pygame.draw.rect(screen, (0, 0, b), blue_band)
         #Render red prompt
        question_surface = font.render(question_r, True, WHITE)
        screen.blit(question_surface, (100, 50))
        #Render user input
        text_surface = font.render(user_text, True, RED)
        screen.blit(text_surface, (100, 75))
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == "__main__":
    main()