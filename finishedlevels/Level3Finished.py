import pygame, sys
from pygame.locals import *
import random
import RockClass
pygame.init()

# Setup screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Load images
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()
flower_image = pygame.image.load("flowerPickUp.png").convert_alpha()
flower_image = pygame.transform.scale(flower_image, (25, 25))
rock_image = pygame.image.load("rock.png").convert_alpha()
# Setup initial position
boppiRect = pygame.Rect(0, 0, 45, 68)

# Background
level1Background = pygame.image.load("backgroundLevel3.png").convert()


# Platforms
platRects = [
    pygame.Rect(-2, 150, 102, 10),
    pygame.Rect(100, 400, 102, 10),
    pygame.Rect(620, 90, 102, 10),
    pygame.Rect(300, 80, 102, 10),
    pygame.Rect(150, 600, 102, 10),
    pygame.Rect(250, 200, 102, 10),
    pygame.Rect(457, 300, 102, 10),
    pygame.Rect(800, 220, 102, 10),
    pygame.Rect(990, 120, 40, 10),
    pygame.Rect(840, 300, 102, 10),
    pygame.Rect(670, 400, 102, 10),
    pygame.Rect(410, 500, 102, 10),
    pygame.Rect(648, 600, 102, 10),
    pygame.Rect(978, 600, 102, 10),
    pygame.Rect(1178, 350, 102, 10),
    pygame.Rect(1208, 500, 72, 10),
    pygame.Rect(70, 380, 30, 10),
]

#Exit Arrow
arrowRect = pygame.Rect(1222.5, 315, 30, 15)

# Flowers
flowerRect_list = [
    pygame.Rect(665, 60, 10, 10),
    pygame.Rect(80, 360, 10, 10),
    pygame.Rect(1005, 100, 10, 10),
    pygame.Rect(870, 260, 10, 10),
    pygame.Rect(195, 570, 10, 10),
    pygame.Rect(1240, 370, 10, 10),
]

flower_locations = [
    (665, 60),
    (80, 360),
    (1005, 100),
    (870, 260),
    (195, 570),
    (1240, 370)
]

#Rocks
rockTimer = 0
rockList = []

# Ground
ground = pygame.Rect(0, 720, 1280, 10)

# Fonts and text
font = pygame.font.Font(None, 30)
lives = 6
flowers = 6
cannotContinueText = font.render("Cannot continue. Collect all of the flowers.", False, (0,0,0))

# Movement vars
velocity_x = 0
velocity_y = 0
on_plat = False
SPEED = 8
JUMP_FORCE = -15
GRAVITY = 1

# Start boppi on first platform
boppiRect.y = platRects[0].top - boppiRect.height

running = True
GameOverFlag = False
level2Flag = False

while running:
    num2 = 0 #used for the flowers
    rockTimer += 1
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Input
    keys = pygame.key.get_pressed()
    velocity_x = 0
    if keys[K_a] or keys[K_LEFT]:
        velocity_x = -SPEED
    if keys[K_d] or keys[K_RIGHT]:
        velocity_x = SPEED
    if (keys[K_SPACE] or keys[K_UP]) and on_plat:
        velocity_y = JUMP_FORCE
        on_plat = False

    # Apply gravity
    velocity_y += GRAVITY
    if velocity_y > 20:
        velocity_y = 20

    # Horizontal movement
    boppiRect.x += velocity_x
    for plat in platRects:
        if boppiRect.colliderect(plat):
            if velocity_x > 0:
                boppiRect.right = plat.left
            elif velocity_x < 0:
                boppiRect.left = plat.right

    #keeping inside:
        if boppiRect.left < 0:
            boppiRect.left = 0
    if boppiRect.right > 1280:
        boppiRect.right = 1280

    # Prevent going off-screen vertically
    if boppiRect.top < 0:
        boppiRect.top = 0
    if boppiRect.bottom > ground.top:
        boppiRect.bottom = ground.top
        velocity_y = 0
        on_plat = True

    # Vertical movement
    boppiRect.y += velocity_y
    on_plat = False
    for plat in platRects:
        if boppiRect.colliderect(plat):
            if velocity_y > 0:
                boppiRect.bottom = plat.top
                velocity_y = 0
                on_plat = True
            elif velocity_y < 0:
                boppiRect.top = plat.bottom
                velocity_y = 0

    # Ground collision
    if boppiRect.bottom >= ground.top:
        boppiRect.bottom = ground.top
        velocity_y = 0
        on_plat = True
        lives -= 1
        boppiRect = pygame.Rect(0, 0, 45, 68)
        screen.blit(boppi, (0,47))
        pygame.display.flip()

    # Top screen limit
    if boppiRect.top < -50:
        boppiRect.top = -50

    #Check to see if flowers picked up
    for flower in flowerRect_list:
        if boppiRect.colliderect(flower):
            flowers = flowers - 1
            del flowerRect_list[num2]
            del flower_locations[num2]
            pygame.display.flip()
        num2 = num2 + 1

    # if player tries to exit screen, checks to see if all flowers have been collected
    if boppiRect.colliderect(arrowRect):
        if flowers == 0:
            level2Flag = True
            sys.exit() #THIS MUST BE REMOVED FOR FULL GAME
        elif flowers != 0:
            level1Background.blit(cannotContinueText, (650, 700))
            pygame.display.flip()
        level1Background.blit(cannotContinueText, (650, 800))
        pygame.display.flip()

    #If player dies
    if lives == 0:
        GameOverFlag = True
        lives = 6
        flowerRect_list = [
            pygame.Rect(665, 60, 10, 10),
            pygame.Rect(80, 360, 10, 10),
            pygame.Rect(1005, 100, 10, 10),
            pygame.Rect(870, 260, 10, 10),
            pygame.Rect(195, 570, 10, 10),
            pygame.Rect(1240, 370, 10, 10),
        ]
        flowers = 6

    # Draw everything
    screen.blit(level1Background, (0, 0))

    # Draw platforms
    for plat in platRects:
        pygame.draw.rect(screen, (0, 100, 0), plat)

    # Draw flowers
    for location in flower_locations:
        screen.blit(flower_image, location)

    screen.blit(arrow, (1222.5, 315))



    # Draw ground
    pygame.draw.rect(screen, (0, 0, 0), ground)

    # Draw Boppi
    screen.blit(boppi, boppiRect.topleft)

    # Optional: draw blue outline to debug Boppi hitbox
    # pygame.draw.rect(screen, (0, 0, 255), boppiRect, 2)

    # Draw text
    screen.blit(font.render(f"Lives: {lives}", True, (0, 0, 0)), (1120, 680))
    screen.blit(font.render(f"Flowers: {flowers}", True, (0, 0, 0)), (1120, 700))


    #causing rocks to spawn
    if rockTimer % 90 == 0:
        newRock = RockClass.Rock()
        rockList.append(newRock)
        #newRock.spawnSound.play()

    for i in rockList:
        RockClass.Rock.draw(i, screen)
        RockClass.Rock.fall(i)
        if i.rect.midbottom == 800-i.rect.height:
            rockList.remove(i)
        if pygame.Rect.colliderect(i.rect, boppiRect):
            lives -= 1
            boppiRect = pygame.Rect(0, 0, 45, 68)
            screen.blit(boppi, (0, 47))
            rockList.remove(i)

    pygame.display.flip()