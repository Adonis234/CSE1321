import pygame, sys
import random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Screen settings
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Level 4")

# Load images
boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()
level4background = pygame.image.load("backgroundLevel4.png").convert_alpha()
level4background = pygame.transform.scale(level4background, (1280,720))

#Load sounds and music
jump = pygame.mixer.Sound('Jump.mp3')
flower_sound = pygame.mixer.Sound('pick up.mp3')
flower_sound.set_volume(0.5)
jump.set_volume(0.5)
#pygame.mixer.music.load('level4sound.mp3')
#pygame.mixer.music.play(-1)

# Font
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 36)

# Setup initial position
boppiRect = pygame.Rect(0, 0, 45, 68)

# Ground
ground = pygame.Rect(0, 720, 1280, 10)

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

#Exit Arrow
arrowRect = pygame.Rect(1222.5, 315, 30, 15)

# Spike class
class Spike:
    def __init__(self, x, y):
        self.width = 30
        self.height = 15  # Smaller hitbox
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x + 5, y + 5, self.width - 10, self.height - 5)

    def draw(self, surface):
        pygame.draw.polygon(surface, (0,0,0), [
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            (self.x + self.width // 2, self.y)
        ])

# Game loop
running = True
while running:
    # Fonts and text
    font = pygame.font.SysFont("Arial", 36, bold=True)
    lives = 6
    flowers = 6
    showMessage = False
    messageTimer = 0
    cannotContinueText = font.render("Cannot continue. Collect all of the flowers!", True, (255, 255, 255))

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
            jump.play()

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
            screen.blit(boppi, (0, 47))
            pygame.display.flip()

        # If player dies
        if lives == 0:
            GameOverFlag = True
            sys.exit() #remove for full game

        # Draw everything
        screen.blit(level4background, (0, 0))

        # Draw platforms
        for plat in platRects:
            pygame.draw.rect(screen, (0, 51, 0), plat)

        screen.blit(arrow, (1222.5, 315))

        # Draw ground
        pygame.draw.rect(screen, (0, 0, 0), ground)

        # Draw Boppi
        screen.blit(boppi, boppiRect.topleft)

        # Draw UI Panel (bottom right)
        hud_width = 150
        hud_height = 40
        hud_x = screen.get_width() - hud_width - 20
        hud_y = screen.get_height() - hud_height - 20
        pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)

        # Fonts
        title_font = pygame.font.Font(None, 34)
        value_font = pygame.font.Font(None, 34)

        # Render Lives text
        lives_text = title_font.render(f"Lives:", True, (255, 102, 255))
        lives_value = value_font.render(str(lives), True, (255, 102, 255))

        # Blit Lives
        screen.blit(lives_text, (hud_x + 10, hud_y + 10))
        screen.blit(lives_value, (hud_x + 120, hud_y + 10))


        pygame.display.flip()

#lets wait until it is all done first