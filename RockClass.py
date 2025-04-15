import random
import pygame
from pygame.locals import*
pygame.init()

class Rock:
    def __init__(self):
        self.speed = 5
        self.sprite = pygame.image.load("rock.png").convert_alpha()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (random.randint(0, 1280-self.rect.width), 0)
       # self.spawnSound = INSERT PATH TO ROCK SOUND

    def fall(self):
        self.rect = self.rect.move(0,self.speed)

    def draw(self, target):
        target.blit(self.sprite, self.rect)
