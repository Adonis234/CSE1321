iimport pygame, sys, random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Level 4")

boppi = pygame.image.load("BoppiFront2.png").convert_alpha()
arrow = pygame.image.load("ArrowNextLevel.png").convert_alpha()
level4background = pygame.image.load("backgroundLevel4.png").convert_alpha()
level4background = pygame.transform.scale(level4background, (1280, 720))
spike_image = pygame.image.load("spike.png").convert_alpha()

jump = pygame.mixer.Sound('Jump.mp3')
flower_sound = pygame.mixer.Sound('pick up.mp3')
flower_sound.set_volume(0.5)
jump.set_volume(0.5)

font = pygame.font.Font(None, 60)

ground = pygame.Rect(0, 720, 1280, 10)

platRects = [
    pygame.Rect(100, 100, 170, 10),
    pygame.Rect(240, 440, 150, 10),
    pygame.Rect(348, 200, 150, 10),
    pygame.Rect(538, 300, 150, 10),
    pygame.Rect(800, 220, 150, 10),
    pygame.Rect(698, 400, 150, 10),
    pygame.Rect(443, 500, 150, 10),
    pygame.Rect(1010, 545, 400, 10),
    pygame.Rect(900, 350, 150, 10),
    pygame.Rect(0, 545, 230, 10),
]

arrowRect = pygame.Rect(1222.5, 520, 30, 15)

class Spike:
    def __init__(self, platform_rect, image):
        self.image = image
        self.platform = platform_rect
        self.x = platform_rect.x
        self.y = platform_rect.y - image.get_height()
        self.speed = 2
        self.direction = 1
        self.rect = pygame.Rect(self.x, self.y, image.get_width(), image.get_height())

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= self.platform.left or self.x + self.rect.width >= self.platform.right:
            self.direction *= -1
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

def get_random_spawn():
    platform = random.choice([platRects[0], platRects[9]])
    return pygame.Rect(platform.x + 10, platform.y - 68, 45, 68)

spikes = []
for i, plat in enumerate(platRects):
    if i in [0, 9]:  # No spikes on spawn platforms
        continue
    spikes.append(Spike(plat, spike_image))

lives = 6
invincible = False
invincibility_timer = 0
invincibility_duration = 2000  # in milliseconds

boppiRect = get_random_spawn()

running = True
velocity_x = 0
velocity_y = 0
SPEED = 8
JUMP_FORCE = -15
GRAVITY = 1
on_plat = False

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

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

    velocity_y += GRAVITY
    if velocity_y > 20:
        velocity_y = 20

    boppiRect.x += velocity_x
    for plat in platRects:
        if boppiRect.colliderect(plat):
            if velocity_x > 0:
                boppiRect.right = plat.left
            elif velocity_x < 0:
                boppiRect.left = plat.right

    boppiRect.left = max(0, boppiRect.left)
    boppiRect.right = min(1280, boppiRect.right)

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

    if boppiRect.bottom >= ground.top:
        lives -= 1
        boppiRect = get_random_spawn()
        invincible = True
        invincibility_timer = pygame.time.get_ticks()

    if not invincible:
        for spike in spikes:
            if boppiRect.colliderect(spike.rect):
                lives -= 1
                boppiRect = get_random_spawn()
                invincible = True
                invincibility_timer = pygame.time.get_ticks()
                break

    if invincible and pygame.time.get_ticks() - invincibility_timer >= invincibility_duration:
        invincible = False

    if lives <= 0:
        sys.exit()

    for spike in spikes:
        spike.move()

    screen.blit(level4background, (0, 0))

    for plat in platRects:
        pygame.draw.rect(screen, (0, 51, 0), plat)

    for spike in spikes:
        spike.draw(screen)

    screen.blit(arrow, (1222.5, 520))
    pygame.draw.rect(screen, (0, 0, 0), ground)

    # Flashing effect if invincible
    if not invincible or (pygame.time.get_ticks() // 200) % 2 == 0:
        screen.blit(boppi, boppiRect.topleft)

    hud_width = 150
    hud_height = 40
    hud_x = screen.get_width() - hud_width - 20
    hud_y = screen.get_height() - hud_height - 20
    pygame.draw.rect(screen, (255, 255, 255), (hud_x, hud_y, hud_width, hud_height), border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), (hud_x, hud_y, hud_width, hud_height), 2, border_radius=10)
    title_font = pygame.font.Font(None, 34)
    value_font = pygame.font.Font(None, 34)
    lives_text = title_font.render(f"Lives:", True, (255, 102, 255))
    lives_value = value_font.render(str(lives), True, (255, 102, 255))
    screen.blit(lives_text, (hud_x + 10, hud_y + 10))
    screen.blit(lives_value, (hud_x + 120, hud_y + 10))

    pygame.display.flip()

pygame.quit()
