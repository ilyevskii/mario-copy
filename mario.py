from pygame import *
import pyganim
import pygame
from time import sleep

WIDTH = 41
HEIGHT = 60
MOVE_SPEED = 3.5
JUMP_POWER = 11
GRAVITY = 0.35
ANIMATION_DELAY = 55
COLOR = (0, 0, 0)

LEFT_POSE = image.load("images/marioLeft.png")
RIGHT_MOVE_ANIMATION = [("images/marioRight_0.png"), ("images/marioRight_1.png"),
              ("images/marioRight_2.png"), ("images/marioRight_3.png")]

LEFT_MOVE_ANIMATION = [("images/marioLeft_0.png"), ("images/marioLeft_1.png"),
              ("images/marioLeft_2.png"), ("images/marioLeft_3.png")]

STAY_ANIMATION = [('images/marioRight_0.png', ANIMATION_DELAY)]
JUMP_LEFT_ANIMATION = [('images/marioJumpLeft.png', ANIMATION_DELAY)]
JUMP_RIGHT_ANIMATION = [('images/marioJumpRight.png', ANIMATION_DELAY)]



class Mario(sprite.Sprite):

    def __init__(self, x, y):
        # Инициализация главного персонажа
        super().__init__()

        self.image = LEFT_POSE
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.onGround = False
        self.onTube = False
        self.x_speed = 0
        self.y_speed = 0
        self.coins = 0
        self.lives = 1

        self.image.set_colorkey(Color(COLOR))
        # Анимация движения вправо
        boltAnim = []
        for anim in RIGHT_MOVE_ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        # Анимация движения влево
        boltAnim = []
        for anim in LEFT_MOVE_ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))

        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(STAY_ANIMATION)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(JUMP_LEFT_ANIMATION)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(JUMP_RIGHT_ANIMATION)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(STAY_ANIMATION)
        self.boltAnimJump.play()

    def update(self, moves, platforms, coins, mobs, spec_platforms, sewers, stairs, flours):
        # Изменение позиции персонажа

        # moves - результат работы файла events.
        movingLeft = moves[0]
        movingRight = moves[1]
        movingUp = moves[2]

        # Проверка, упал ли вниз карты
        if 800 < self.rect.bottom < 811:
            self.lives -= 1

        if movingRight:
            self.x_speed = MOVE_SPEED
            self.image.fill(Color(COLOR))

            if self.y_speed != 0.7 and self.y_speed != 0.35 and self.y_speed != 0:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if movingLeft:
            self.x_speed = -MOVE_SPEED
            self.image.fill(Color(COLOR))

            if self.y_speed != 0.7 and self.y_speed != 0.35 and self.y_speed != 0:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if not movingRight and not movingLeft:
            self.x_speed = 0
            self.boltAnimStay.blit(self.image, (0, 0))

            self.image.fill(Color(COLOR))
            self.boltAnimStay.blit(self.image, (0, 0))

        if movingUp:
            if self.onGround:
                jump_sound = pygame.mixer.Sound('music/jump.wav')
                jump_sound.play(0)
                self.y_speed -= JUMP_POWER
                self.onGround = False

        if not self.onGround:
            self.y_speed += GRAVITY

        self.onTube = False
        self.onGround = False


        self.rect.centery += self.y_speed
        self.check_for_collide(0, self.y_speed, platforms, coins, mobs, spec_platforms, sewers, stairs, flours)

        self.rect.centerx += self.x_speed
        self.check_for_collide(self.x_speed, 0, platforms, coins, mobs, spec_platforms, sewers, stairs, flours)

    def check_for_collide(self, x_speed, y_speed, platforms, coins, mobs, spec_platforms, sewers, stairs, flours):

        # Проверка на столкновения с блоками с вопросами
        for block in spec_platforms:

            if sprite.collide_rect(self, block):

                if not self.onGround and self.rect.bottom >= block.rect.top + 10:

                    if block.rect.left < self.rect.centerx < block.rect.right:
                        self.y_speed = -1
                        spec_platforms.remove(block)

                    else:
                        get_collide(self, block, x_speed, y_speed)
                else:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.y_speed = 0

        # Проверка на столкновения с блоками
        for block in platforms:

            if sprite.collide_rect(self, block):

                get_collide(self, block, x_speed, y_speed)

        for block in stairs:

            if sprite.collide_rect(self, block):
                get_collide(self, block, x_speed, y_speed)

        for block in flours:

            if sprite.collide_rect(self, block):
                get_collide(self, block, x_speed, y_speed)

        # Проверка на столкновения с монетами
        for coin in coins:

            if sprite.collide_rect(self, coin):
                self.coins += 1
                coins.remove(coin)

        # Проверка на столкновения с мобами
        for mob in mobs:

            if sprite.collide_rect(self, mob):

                if not self.onGround and self.rect.bottom <= mob.rect.top + 10:

                    # sleep(0.25)
                    mobs.remove(mob)
                else:
                    if self.lives > 0:
                        self.lives -= 1

        # Проверка на столкновения с трубами
        for sewer in sewers:

            if sprite.collide_rect(self, sewer):

                get_collide(self, sewer, x_speed, y_speed)
                if y_speed > 0:
                    self.onTube = True



def get_collide(mario, block, x_speed, y_speed):
    if x_speed > 0:
        mario.rect.right = block.rect.left

    if x_speed < 0:
        mario.rect.left = block.rect.right

    if y_speed < 0:
        mario.rect.top = block.rect.bottom
        mario.y_speed = 0

    if y_speed > 0:
        mario.rect.bottom = block.rect.top
        mario.onGround = True
        mario.y_speed = 0

