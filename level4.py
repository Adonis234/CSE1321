import pygame
import random
from pygame.locals import *
from sound import level4sound

pygame.init()
clock = pygame.time.Clock()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boppi Movement Inside Brown Ground")

# Colors
brown = (139, 69, 19)
blue = (173, 216, 230)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)  # Black color for the text

# Font
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 36)

# Brown ground settings
stripe_height = 200
stripe_y = screen_height // 2 - stripe_height // 2
stripe_bottom = stripe_y + stripe_height

# Load and scale image
boppi_image = pygame.image.load("BoppiFront.png").convert_alpha()
boppi_image = pygame.transform.scale(boppi_image, (50, 70))

# Jump sound
jump_sound = pygame.mixer.Sound("Jump.mp3")  # Add your jump sound file

# Platform class
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, white, self.rect)

# Spike class
class Spike:
    def __init__(self, x, y):
        self.width = 30
        self.height = 15  # Smaller hitbox
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x + 5, y + 5, self.width - 10, self.height - 5)

    def draw(self, surface):
        pygame.draw.polygon(surface, red, [
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            (self.x + self.width // 2, self.y)
        ])

# Platforms and spikes
platforms = [
    Platform(100, stripe_y + 100, 170, 10),
    Platform(350, stripe_y + 120, 160, 10),
    Platform(600, stripe_y + 100, 150, 10),
]

spikes = [
    Spike(platform.rect.centerx - 15, platform.rect.top - 15) for platform in platforms
]

# Create additional spikes on the bottom of the brown ground
bottom_spikes = []
for x in range(0, screen_width, 35):
    if x < 100 or x > screen_width - 100:  # Exclude spawn and end areas
        continue
    bottom_spikes.append(Spike(x, stripe_bottom - 15))  # Place spikes on the bottom ground

# Create next level arrow at the end of the brown ground (smaller size)
arrow_image = pygame.image.load("arrow.png").convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (30, 30))  # Make the arrow smaller
arrow_rect = pygame.Rect(screen_width - 100, stripe_y + 50, 30, 30)

def reset_game():
    global boppiRect, player_health, is_hurt, hurt_time, game_over, velocity_y, on_ground, level_complete
    boppiRect = boppi_image.get_rect()
    boppiRect.bottomleft = (0, stripe_y + stripe_height)  # Spawn on far left of brown ground
    player_health = 100
    is_hurt = False
    hurt_time = 0
    game_over = False
    level_complete = False
    velocity_y = 0
    on_ground = False

# Initialize game state
reset_game()
level4sound()

# Game loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if game_over:
                if event.key == K_r:
                    reset_game()
                elif event.key == K_ESCAPE:
                    running = False

    if not game_over and not level_complete:
        keys = pygame.key.get_pressed()
        velocity_x = 0
        if keys[K_a] or keys[K_LEFT]:
            velocity_x = -4
        if keys[K_d] or keys[K_RIGHT]:
            velocity_x = 4
        if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and on_ground:
            velocity_y = -10  # Increased jump height
            jump_sound.play()  # Play jump sound when player jumps

        # Gravity
        velocity_y += 0.5
        if velocity_y > 10:
            velocity_y = 10

        # Move
        boppiRect.x += velocity_x
        boppiRect.y += velocity_y

        # Horizontal bounds
        if boppiRect.left < 0:
            boppiRect.left = 0
        if boppiRect.right > screen_width:
            boppiRect.right = screen_width

        # Platform collision (prevent jumping through platforms)
        on_ground = False
        for plat in platforms:
            if boppiRect.colliderect(plat.rect) and velocity_y >= 0:  # Only allow player to land on platform from below
                boppiRect.bottom = plat.rect.top
                velocity_y = 0
                on_ground = True

        # Brown ground collision
        if boppiRect.bottom >= stripe_bottom:
            boppiRect.bottom = stripe_bottom
            velocity_y = 0
            on_ground = True

        # Collision with spikes on platforms
        for spike in spikes:
            if boppiRect.colliderect(spike.rect) and not is_hurt:
                player_health -= 25
                is_hurt = True
                hurt_time = current_time
                boppiRect.x -= 50
                if boppiRect.left < 0:
                    boppiRect.left = 0

        # Collision with bottom spikes (only the spikes on the bottom)
        for spike in bottom_spikes:
            if boppiRect.colliderect(spike.rect) and not is_hurt:
                player_health = 0  # Set health to 0, which will end the game
                is_hurt = True
                hurt_time = current_time
                boppiRect.x -= 50
                if boppiRect.left < 0:
                    boppiRect.left = 0

        # Collision with next arrow for next level
        if boppiRect.colliderect(arrow_rect):
            level_complete = True

        if is_hurt and current_time - hurt_time > 1000:
            is_hurt = False

        if player_health <= 0:
            game_over = True

    # Drawing
    screen.fill(blue)
    pygame.draw.rect(screen, brown, (0, stripe_y, screen_width, stripe_height))

    for plat in platforms:
        plat.draw(screen)

    for spike in spikes:
        spike.draw(screen)

    # Draw bottom spikes
    for spike in bottom_spikes:
        spike.draw(screen)

    # Draw the next level arrow
    if not level_complete:
        screen.blit(arrow_image, arrow_rect)

    if not game_over and not level_complete:
        screen.blit(boppi_image, boppiRect)
        health_text = small_font.render(f"Health: {player_health}", True, black)  # Change text color to black
        screen.blit(health_text, (10, 10))

        if is_hurt:
            hurt_text = small_font.render("Boppi Got Hurt!", True, black)  # Change text color to black
            screen.blit(hurt_text, (screen_width // 2 - hurt_text.get_width() // 2, 50))

    elif level_complete:
        # Display the message for completing the level in black
        good_job_text = font.render("Good Job! Next Level", True, black)  # Change text color to black
        screen.blit(good_job_text, (
            screen_width // 2 - good_job_text.get_width() // 2,
            screen_height // 2 - good_job_text.get_height()
        ))
        retry_text = small_font.render("Press R to go on", True, black)  # Change text color to black
        screen.blit(retry_text, (
            screen_width // 2 - retry_text.get_width() // 2,
            screen_height // 2 + 10
        ))

    elif game_over:
        over_text = font.render("GAME OVER", True, black)  # Change text color to black
        screen.blit(over_text, (
            screen_width // 2 - over_text.get_width() // 2,
            screen_height // 2 - over_text.get_height()
        ))
        retry_text = small_font.render("Press R to Try Again or ESC to Quit", True, black)  # Change text color to black
        screen.blit(retry_text, (
            screen_width // 2 - retry_text.get_width() // 2,
            screen_height // 2 + 10
        ))

    pygame.display.flip()

pygame.quit()





