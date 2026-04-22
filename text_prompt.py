import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 24)

user_text = ""
question = "R[0-255]: "

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("User entered:", user_text)
                user_text = ""
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    # Render question
    question_surface = font.render(question, True, (255, 255, 255))
    screen.blit(question_surface, (50, 100))

    # Render user input
    text_surface = font.render(user_text, True, (255, 0, 0))
    screen.blit(text_surface, (50, 150))

    # Render Rectangles

    #Activate text prompt when box is clicked. User must enter num and can be max 3 digits & within range.

    pygame.display.flip()

pygame.quit()