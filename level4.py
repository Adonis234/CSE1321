import pygame
import random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boppi Movement Inside Brown Ground")

# Game variables
speed = 4
velocity_x = 0
velocity_y = 0
spike_timer = 0
hurt_time = 0
is_hurt = False

# Load and scale image
boppi = pygame.image.load("BoppiFront.png").convert_alpha()
boppi = pygame.transform.scale(boppi, (50, 70))

# Get the Rect for positioning
boppiRect = boppi.get_rect()
boppiRect.midleft = (0, screen_height // 2)

# Colors
brown = (139, 69, 19)
blue = (173, 216, 230)
red = (255, 0, 0)

# Font
font = pygame.font.SysFont(None, 60)

# Brown ground settings
stripe_height = 200
stripe_y = screen_height // 2 - stripe_height // 2
stripe_bottom = stripe_y + stripe_height

# Spike class
class Spike:
    def __init__(self, x, y):
        self.width = 30
        self.height = 20
        self.x = x
        self.y = y
        self.spawn_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.polygon(surface, red, [
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            (self.x + self.width // 2, self.y)
        ])

# List of spikes
spikes = []

def create_spike():
    x = random.randint(0, screen_width - 30)
    y = random.randint(stripe_y, stripe_bottom - 20)
    spikes.append(Spike(x, y))

# Game loop
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input only if not hurt
    if not is_hurt:
        keys = pygame.key.get_pressed()
        velocity_x = 0
        if keys[K_a] or keys[K_LEFT]:
            velocity_x = -speed
        if keys[K_d] or keys[K_RIGHT]:
            velocity_x = speed
        if keys[K_UP]:
            velocity_y = -speed
        elif keys[K_DOWN]:
            velocity_y = speed
        else:
            velocity_y = 0

        # Move Boppi
        boppiRect.x += velocity_x
        boppiRect.y += velocity_y

    # Keep Boppi in brown area
    if boppiRect.left < 0:
        boppiRect.left = 0
    if boppiRect.top < stripe_y:
        boppiRect.top = stripe_y
    if boppiRect.bottom > stripe_bottom:
        boppiRect.bottom = stripe_bottom

    # Make spikes randomly appear
    if current_time - spike_timer > random.randint(1000, 2000):
        create_spike()
        spike_timer = current_time

    # Remove spikes after 2 seconds
    spikes = [spike for spike in spikes if current_time - spike.spawn_time < 2000]

    # Check for collision
    for spike in spikes:
        if boppiRect.colliderect(spike.rect) and not is_hurt:
            hurt_time = current_time
            is_hurt = True
            # Push Boppi back
            boppiRect.x -= 50
            if boppiRect.left < 0:
                boppiRect.left = 0

    # Stop movement for 1 second after hurt
    if is_hurt and current_time - hurt_time > 1000:
        is_hurt = False

    # Draw scene
    screen.fill(blue)
    pygame.draw.rect(screen, brown, (0, stripe_y, screen_width, stripe_height))
    screen.blit(boppi, boppiRect)

    for spike in spikes:
        spike.draw(screen)

    # Hurt message
    if is_hurt:
        text = font.render("Boppi Got Hurt!", True, red)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50))

    pygame.display.flip()

pygame.quit()





