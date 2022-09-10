import pygame.image
from pygame import *
import pyganim
from time import sleep

WIDTH = 39
HEIGHT = 45
MOVE_SPEED = 3
GRAVITY = 0.525
ANIMATION_DELAY = 70
COLOR = (90, 90, 90)

MOB_ANIMATION  = [("images/mobLeft.png"), ("images/mobRight.png")]
MOB_DEAD_ANIMATION = [("images/mobDead.png", ANIMATION_DELAY)]


class Mob(sprite.Sprite):

    def __init__(self, x, y):
        # Инициализация моба
        sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/mobLeft.png')
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.onGround = False
        self.x_speed = MOVE_SPEED
        self.y_speed = 0
        self.is_alive = True

        boltAnim = []
        for anim in MOB_ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimSpec = pyganim.PygAnimation(boltAnim)
        self.boltAnimSpec.play()

        self.boltAnimDead = pyganim.PygAnimation(MOB_DEAD_ANIMATION)
        self.boltAnimDead.play()

    def update(self, platforms, sewers, stairs, flours):
        # Изменение позиции моба

        if not self.onGround:
            self.y_speed += GRAVITY

        self.onGround = False

        self.rect.centery += self.y_speed
        self.check_for_collide(0, self.y_speed, platforms, sewers, stairs, flours)

        self.rect.centerx += self.x_speed
        self.check_for_collide(self.x_speed, 0, platforms, sewers, stairs, flours)

        self.image.fill(Color(COLOR))

        if self.is_alive:
            self.boltAnimSpec.blit(self.image, (0, 0))
        else:
            self.boltAnimDead.blit(self.image, (0, 0))


    def check_for_collide(self, x_speed, y_speed, platforms, sewers, stairs, flours):
        # Проверка на столкновения с блоками
        for block in platforms:
            if sprite.collide_rect(self, block):
                get_collide(self, block, x_speed, y_speed)

        # Проверка на столкновения с трубами
        for sewer in sewers:
            if sprite.collide_rect(self, sewer):
                get_collide(self, sewer, x_speed, y_speed)

        # Проверка на столкновения с лестницами
        for stair in stairs:
            if sprite.collide_rect(self, stair):
                get_collide(self, stair, x_speed, y_speed)

        for flour in flours:
            if sprite.collide_rect(self, flour):
                get_collide(self, flour, x_speed, y_speed)


def get_collide(mob, block, x_speed, y_speed):
    if x_speed > 0:
        mob.rect.right = block.rect.left
        mob.x_speed = -mob.x_speed

    if x_speed < 0:
        mob.rect.left = block.rect.right
        mob.x_speed = -mob.x_speed

    if y_speed > 0:
        mob.rect.bottom = block.rect.top
        mob.onGround = True
        mob.y_speed = 0


def update_mobs(mobs, platforms, sewers, stairs, flours):
    #Обновляем список мобов

    for mob in mobs:
        if mob.is_alive:
            mob.update(platforms, sewers, stairs, flours)
        else:
            mobs.remove(mob)
