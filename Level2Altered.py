import pygame, sys
from pygame.locals import *

pygame.init()

# Setup screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Load images
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()

# Position first
boppiRect = pygame.Rect(0, 0, 45, 68)

# Background - with waterfall area marked
level2Background = pygame.Surface((1280, 720))
level2Background.fill((204, 255, 204))
# waterfall
pygame.draw.rect(level2Background, (100, 150, 255), (400, 0, 480, 720))

# Waterfall platforms (in center)
waterfall_platRects = [
    pygame.Rect(450, 60, 100, 10),
    pygame.Rect(590, 180, 100, 10),
    pygame.Rect(730, 60, 100, 10),
    pygame.Rect(450, 300, 100, 10),
    pygame.Rect(590, 420, 100, 10),
    pygame.Rect(730, 300, 100, 10),
    pygame.Rect(450, 540, 100, 10),
    pygame.Rect(590, 660, 100, 10),
    pygame.Rect(730, 540, 100, 10),
]

#  left side
left_platRects = [
    pygame.Rect(0, 330, 100, 10), #starting platform
    pygame.Rect(150, 230 , 100, 10),
    pygame.Rect(270, 140, 100, 10),
    pygame.Rect(20, 120, 100, 10),
    pygame.Rect(80, 510, 100, 10),
    pygame.Rect(270, 420, 100, 10),
    pygame.Rect(270, 600, 100, 10),
]

# on right side
right_platRects = [
    pygame.Rect(1100, 120, 100, 10),
    pygame.Rect(900, 220, 100, 10),
    pygame.Rect(1180, 350, 100, 10), #arrow platform
    pygame.Rect(900, 550, 100, 10),
    pygame.Rect(1020, 450, 100, 10),
    pygame.Rect(1150, 650, 100, 10),
]

# Combine all platforms for collision detection
all_platRects = left_platRects + waterfall_platRects + right_platRects

# Original waterfall
original_waterfall_positions = [rect.y for rect in waterfall_platRects]

# Exit Arrow
arrowRect = pygame.Rect(1220, 315, 30, 15)

# Flowers
flowerRect_list = [
    pygame.Rect(190, 35, 10, 10),  # Left side
    pygame.Rect(500, 35, 10, 10),  # Waterfall
    pygame.Rect(1145, 65, 10, 10),  # Right side
    pygame.Rect(635, 540, 10, 10),  # Waterfall
    pygame.Rect(125, 475, 10, 10),  # Left side
    pygame.Rect(1195, 610, 10, 10),  # Right side
]

# Ground
ground = pygame.Rect(0, 720, 1280, 10)

# Fonts and text
font = pygame.font.Font(None, 30)
lives = 6
flowers = 6
cannotContinueText = font.render("Cannot continue. Collect all of the flowers.", False, (0, 0, 0))
waterfallWarningText = font.render("You can't fall or hit the bottom in the waterfall!", False, (255, 255, 255))
mistWarningText = font.render("Cannot advance. Collect all the flowers!!", False, (255, 255, 255))

# Movement vars
velocity_x = 0
velocity_y = 0
on_plat = False
SPEED = 8
JUMP_FORCE = -15
GRAVITY = 1
WATERFALL_SPEED = 1  # How fast waterfall platforms move down
MIST_FORCE = -5  # Upward force when trying to advance without flowers

# starting point
boppiRect.midbottom = left_platRects[0].midtop

running = True
GameOverFlag = False
level3Flag = False
show_warning = False
warning_timer = 0
show_mist_warning = False
mist_timer = 0

while running:
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

    # Downwards only
    for plat in waterfall_platRects:
        plat.y += WATERFALL_SPEED
        # Reset platform to top when it goes off screen
        if plat.top > 720:
            plat.y = -0.001

    # Flower movement - only waterfall flowers move
    for i, flower in enumerate(flowerRect_list):
        # Check if flower is in waterfall area (x between 400-880)
        if 400 <= flower.x <= 880:
            for plat in waterfall_platRects:
                if abs(flower.x - plat.centerx) < 60:  # Rough association
                    flower.y = plat.y - 15  # Keep above platform
                    break

    # Horizontal movement
    boppiRect.x += velocity_x
    for plat in all_platRects:
        if boppiRect.colliderect(plat):
            if velocity_x > 0:
                boppiRect.right = plat.left
            elif velocity_x < 0:
                boppiRect.left = plat.right

    # Keep inside screen horizontally
    if boppiRect.left < 0:
        boppiRect.left = 0
    if boppiRect.right > 1280:
        boppiRect.right = 1280

    # Prevent going above screen
    if boppiRect.top < -80:
        boppiRect.top = -80
        velocity_y = 0

    # Vertical movement
    boppiRect.y += velocity_y
    on_plat = False
    for plat in all_platRects:
        if boppiRect.colliderect(plat):
            if velocity_y > 0:
                boppiRect.bottom = plat.top
                velocity_y = 0
                on_plat = True
            elif velocity_y < 0:
                boppiRect.top = plat.bottom
                velocity_y = 0

    # Check if player falls below screen (waterfall bottom)
    if boppiRect.top > 720:
        lives -= 1
        if lives <= 0:
            pygame.quit()
            sys.exit()
        # Reset position to starting platform
        boppiRect.midbottom = left_platRects[0].midtop
        # Reset waterfall platforms to original positions
        for i, plat in enumerate(waterfall_platRects):
            plat.y = original_waterfall_positions[i]
        # Show warning message
        #show_warning = True
        warning_timer = 180  # 3 seconds at 60fps

    # Flower collection
    for flower in flowerRect_list[:]:  # Make a copy for iteration
        if boppiRect.colliderect(flower):
            flowers -= 1
            flowerRect_list.remove(flower)
            pygame.display.flip()

    # Check for level completion (arrow on right side)
    if boppiRect.colliderect(arrowRect):
        if flowers == 0:
            level3Flag = True
            running = False
        else:
            # Apply mist force (push player up)
            velocity_y = MIST_FORCE
            # Show mist warning
            show_mist_warning = True
            mist_timer = 120  # 2 seconds

    # Warning message timers
    if show_warning:
        warning_timer -= 1
        if warning_timer <= 0:
            show_warning = False

    if show_mist_warning:
        mist_timer -= 1
        if mist_timer <= 0:
            show_mist_warning = False

    #  everything
    screen.blit(level2Background, (0, 0))

    #  left platforms (green)
    for plat in left_platRects:
        pygame.draw.rect(screen, (0, 51, 0), plat)

    #  waterfall platforms (blue)
    for plat in waterfall_platRects:
        pygame.draw.rect(screen, (0, 100, 200), plat)

    #  right platforms (green)
    for plat in right_platRects:
        pygame.draw.rect(screen, (0, 51, 0), plat)

    #  flowers
    for flower in flowerRect_list:
        pygame.draw.rect(screen, (255, 102, 178), flower)

    screen.blit(arrow, arrowRect.topleft)

    #  Boppi
    screen.blit(boppi, boppiRect.topleft)

    #  text
    screen.blit(font.render(f"Lives: {lives}", True, (0, 0, 0)), (1120, 680))
    screen.blit(font.render(f"Flowers: {flowers}", True, (0, 0, 0)), (1120, 700))

    # Show warnings if needed
    if show_warning:
        screen.blit(waterfallWarningText, (450, 350))
    if show_mist_warning:
        screen.blit(mistWarningText, (450, 400))

    pygame.display.flip()