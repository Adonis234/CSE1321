import pygame, sys
from pygame.locals import *
pygame.init()

# Setup screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Load images
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()
flower_image = pygame.image.load("flowerPickUp.png").convert_alpha()
flower_image = pygame.transform.scale(flower_image, (25, 25))

# Setup initial position
boppiRect = pygame.Rect(0, 0, 45, 68)

# Background
level1Background = pygame.Surface((1280, 720))
level1Background = pygame.image.load("backgroundLevel1.png")

# Platforms
platRects = [
    pygame.Rect(-2, 150, 102, 10),
    pygame.Rect(198, 250, 102, 10),
    pygame.Rect(58, 350, 102, 10),
    pygame.Rect(198, 550, 102, 10),
    pygame.Rect(98, 70, 102, 10),
    pygame.Rect(348, 200, 102, 10),
    pygame.Rect(538, 300, 102, 10),
    pygame.Rect(800, 220, 102, 10),
    pygame.Rect(990, 120, 102, 10),
    pygame.Rect(698, 400, 102, 10),
    pygame.Rect(443, 500, 102, 10),
    pygame.Rect(648, 600, 102, 10),
    pygame.Rect(978, 600, 102, 10),
    pygame.Rect(1178, 350, 102, 10),
    pygame.Rect(38, 650, 42, 10),
]

flowerRect_list = [
    pygame.Rect(105, 325, 10, 10),
    pygame.Rect(55, 625, 10, 10),
    pygame.Rect(145, 45, 10, 10),
    pygame.Rect(1040, 85, 10, 10),
    pygame.Rect(600, 45, 10, 10),
    pygame.Rect(855, 495, 10, 10),
    ]

#Exit Arrow
arrowRect = pygame.Rect(1222.5, 315, 30, 15)

# Flowers
flower_locations = [
    (95, 315),
    (45, 615),
    (135, 35),
    (1030, 75),
    (590, 35),
    (845, 485)
]

# Ground
ground = pygame.Rect(0, 720, 1280, 10)

# Fonts and text
font = pygame.font.SysFont("Arial", 36, bold=True)
lives = 6
flowers = 6
showMessage = False
messageTimer = 0

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
    num2 = 0
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

    # Keep inside screen
    if boppiRect.left < 0:
        boppiRect.left = 0
    if boppiRect.right > 1280:
        boppiRect.right = 1280

    # Prevent going off-screen vertically
    if boppiRect.top < -80:
        boppiRect.top = -80
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

    # Check to see if flowers picked up
    for flower in flowerRect_list[:]:
        if boppiRect.colliderect(flower):
            flowers -= 1
            index = flowerRect_list.index(flower)
            del flower_locations[index]
            flowerRect_list.remove(flower)

    # if player tries to exit screen, check flowers
    if boppiRect.colliderect(arrowRect):
        if flowers == 0:
            level2Flag = True
            sys.exit()  # REMOVE for full game
        else:
            showMessage = True
            messageTimer = pygame.time.get_ticks()

    # Remove message after 2 seconds
    if showMessage and pygame.time.get_ticks() - messageTimer > 2000:
        showMessage = False

    # If player dies
    if lives == 0:
        GameOverFlag = True
        lives = 6
        flowerRect_list = [
            pygame.Rect(105, 325, 10, 10),
            pygame.Rect(55, 625, 10, 10),
            pygame.Rect(145, 45, 10, 10),
            pygame.Rect(1040, 85, 10, 10),
            pygame.Rect(600, 45, 10, 10),
            pygame.Rect(855, 495, 10, 10),
        ]
        flower_locations = [
            (95, 315),
            (45, 615),
            (135, 35),
            (1030, 75),
            (590, 35),
            (845, 485)
        ]
        flowers = 6

    # Draw everything
    screen.blit(level1Background, (0, 0))

    # Draw platforms
    for plat in platRects:
        pygame.draw.rect(screen, (0, 51, 0), plat)

    # Draw flowers
    for location in flower_locations:
        screen.blit(flower_image, location)

    screen.blit(arrow, (1222.5, 315))

    # Draw ground
    pygame.draw.rect(screen, (0, 0, 0), ground)

    # Draw Boppi
    screen.blit(boppi, boppiRect.topleft)

   # Draw UI Panel (bottom right)
    hud_width = 200
    hud_height = 70
    hud_x = screen.get_width() - hud_width - 20
    hud_y = screen.get_height() - hud_height - 20
    pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)

   # Fonts
    title_font = pygame.font.Font(None, 34)
    value_font = pygame.font.Font(None, 30)

   # Render Lives text
    lives_text = title_font.render(f"Lives:", True, (255, 0, 0))
    lives_value = value_font.render(str(lives), True, (255, 0, 0))

   # Render Flowers text
    flowers_text = title_font.render(f"Flowers:", True, (0, 153, 0))
    flowers_value = value_font.render(str(flowers), True, (0, 153, 0))

   # Blit Lives
    screen.blit(lives_text, (hud_x + 10, hud_y + 10))
    screen.blit(lives_value, (hud_x + 120, hud_y + 10))

   # Blit Flowers
    screen.blit(flowers_text, (hud_x + 10, hud_y + 35))
    screen.blit(flowers_value, (hud_x + 120, hud_y + 35))

    # Show warning message
    if showMessage:
        screen.blit(cannotContinueText, (650, 680))

    pygame.display.flip()
