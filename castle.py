from pygame import *
import pyganim
import pygame


CASTLE_WIDTH = 100
CASTLE_HEIGHT = 100


class Castle(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, CASTLE_WIDTH, CASTLE_HEIGHT)
        picture = pygame.image.load("images/castle.png")
        picture = pygame.transform.scale(picture, (300, 300))
        self.image = picture
