from pygame import *
from time import sleep

WIDTH = 41
HEIGHT = 60
MOVE_SPEED = 3.5
JUMP_POWER = 11
GRAVITY = 0.35
LEFT_POSE = image.load("images/marioLeft.png")
RIGHT_POSE = image.load("images/marioRight.png")

class Mario(sprite.Sprite):

    def __init__(self, x, y):
        # Инициализация главного персонажа
        sprite.Sprite.__init__(self)
        self.image = RIGHT_POSE
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.onGround = False
        self.onTube = False
        self.x_speed = 0
        self.y_speed = 0
        self.coins = 0
        self.lives = 1

    def update(self, moves, platforms, coins, mobs, spec_platforms, sewers):
        # Изменение позиции персонажа

        #moves - результат работы файла events.
        movingLeft = moves[0]
        movingRight = moves[1]
        movingUp = moves[2]

        if movingRight:
            self.x_speed = MOVE_SPEED
            self.image = RIGHT_POSE
        if movingLeft:
            self.x_speed = -MOVE_SPEED
            self.image = LEFT_POSE

        if not movingRight and not movingLeft:
            self.x_speed = 0

        if movingUp:
            if self.onGround:
                self.y_speed -= JUMP_POWER

        if not self.onGround:
            self.y_speed += GRAVITY

        self.onTube = False
        self.onGround = False

        self.rect.centery += self.y_speed
        self.check_for_collide(0, self.y_speed, platforms, coins, mobs, spec_platforms, sewers)

        self.rect.centerx += self.x_speed
        self.check_for_collide(self.x_speed, 0, platforms, coins, mobs, spec_platforms, sewers)


    def check_for_collide(self, x_speed, y_speed, platforms, coins, mobs, spec_platforms, sewers):
        #Проверка на столкновения с блоками
        for block in platforms:

            if sprite.collide_rect(self, block):

                get_collide(self, block, x_speed, y_speed)


        # Проверка на столкновения с монетами
        for coin in coins:

            if sprite.collide_rect(self, coin):
                self.coins += 1
                coins.remove(coin)

        #Проверка на столкновения с мобами
        for mob in mobs:

            if sprite.collide_rect(self, mob):

                if not self.onGround and self.rect.bottom <= mob.rect.top + 10:

                    #sleep(0.25)
                    mobs.remove(mob)
                else:
                    if self.lives > 0:
                        self.lives -= 1

        #Проверка на столкновения с блоками с вопросами
        for block in spec_platforms:

            if sprite.collide_rect(self, block):

                if not self.onGround and self.rect.top >= block.rect.bottom - 20:
                    self.y_speed = -1
                    spec_platforms.remove(block)
                else:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.y_speed = 0

        #Проверка на столкновения с трубами
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

