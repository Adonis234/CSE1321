import pygame

pygame.init()
pygame.mixer.init()

#jumps sound
def jumpsound():
    jump = pygame.mixer.Sound('Jump.mp3')
    jump.play()
    jump.set_volume(0.5)

#when she pick the flower def pickup():
    pickup = pygame.mixer.Sound('pick up.mp3')
    pickup.set_volume(0.5)

#background music
def level2sound():
    pygame.mixer.music.load('level2sound.mp3v.mp3')
    pygame.mixer.music.play(-1)

def level3sound():
    pygame.mixer.music.load('level3sound.mp3')
    pygame.mixer.music.play(-1)


# this can be used for 1 and home screen
def level1sound():
    pygame.mixer.music.load('backgound.mp3')
    pygame.mixer.music.play(-1)

#when something hit or touch her
def hit(self):
    hit = pygame.mixer.Sound("hitsound.mp3")
    hit.set_volume(0.5)

#when he or her dies
def death():
    death=pygame.mixer.Sound("death.mp3")
    death.set_volume(0.9)

# if you wanted to test out the music

level1sound()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               #if you wanted to hear the jump
               jumpsound()
pygame.quit()