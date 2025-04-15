import pygame
import random
from pygame.locals import *
#from sound import level1sound

pygame.init()
clock = pygame.time.Clock()

# Screen settings
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Character Dialogue Box")

# Colors
blue = (173, 216, 230)
brown = (139, 69, 19)
white = (255, 255, 255)

# Font
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Character images (replace these with actual character images)
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
#batti = pygame.image.load("BoppiFront2.png").convert_alpha()  # Replace with actual path
batti = pygame.Surface((45,68))

# Dialogue Box settings
dialogue_box_width = 600
dialogue_box_height = 150
boppi_box_x = 150
boppi_box_y = 150
batti_box_x = 530
batti_box_y = 200

# Dialogue text
d1 = "Hello! How are you doing today?"
d2 = "I'm doing great, thanks for asking!"
d3 = "Boppi 1"
d4 = "Batti 1"
d5 = "Boppi 2"
d6 = "Batti 2"
d7 = "Boppi 3"
d8 = "Batti 3"

# Dialogue list
dialogue = [d1,d2,d3,d4,d5,d6,d7,d8]

# Dialogue states
# True when Boppi is talking, false when batti is talking
boppi_talking = [True, False, True, False, True, False, True, False]



# Character speaking box (rectangle)
boppi_box_rect = pygame.Rect(boppi_box_x, boppi_box_y, dialogue_box_width, dialogue_box_height)
batti_box_rect = pygame.Rect(batti_box_x, batti_box_y, dialogue_box_width, dialogue_box_height)

def draw_dialogue_box(character_image, dialogue_text):
    if boppi_talking[num]:
        pygame.draw.rect(screen, white, boppi_box_rect) # Draw the dialogue box
        pygame.draw.rect(screen, brown, boppi_box_rect, 5)  # Border for the box
        screen.blit(character_image, (boppi_box_x + 10, boppi_box_y + 20)) # Display character image
        text_surface = font.render(dialogue[num], True, (0, 0, 0))  # Display dialogue text inside the box
        screen.blit(text_surface, (boppi_box_x + 80, boppi_box_y + 30))  # Text offset
    elif boppi_talking[num] == False:
        pygame.draw.rect(screen, white, batti_box_rect)  # Draw the dialogue box
        pygame.draw.rect(screen, brown, batti_box_rect, 5)  # Border for the box
        screen.blit(character_image, (batti_box_x + 10, batti_box_y + 20))  # Display character image
        text_surface = font.render(dialogue[num], True, (0, 0, 0))  # Display dialogue text inside the box
        screen.blit(text_surface, (batti_box_x + 80, batti_box_y + 30))  # Text offset

num = 0

# Game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and num <= (len(dialogue) - 1):
                num = num + 1

    # Drawing
    screen.fill(blue)  # Fill the background with blue

    # Draw the dialogue box and character images with the text
    if num <= (len(dialogue) - 1):
        if boppi_talking[num]:
            draw_dialogue_box(boppi, dialogue[num])
        elif boppi_talking[num] == False:
            draw_dialogue_box(batti, dialogue[num])
    elif num == len(dialogue):
        theEnd_box_rect = pygame.Rect(240, 160, 800, 400)
        pygame.draw.rect(screen, white, theEnd_box_rect)  # Draw the dialogue box
        pygame.draw.rect(screen, brown, theEnd_box_rect, 5)  # Border for the box
        theEnd_text = font.render("THE END.", True, (0, 0, 0))  # Display dialogue text inside the box
        screen.blit(theEnd_text, (570, 190))  # Text offset

    pygame.display.flip()

pygame.quit()