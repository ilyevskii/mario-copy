from pygame import *

WIDTH = 39
HEIGHT = 45
MOVE_SPEED = 3.5
GRAVITY = 0.525
LEFT_POSE = image.load("images/mobLeft.png")
RIGHT_POSE = image.load("images/mobRight.png")

class Mob(sprite.Sprite):

    def __init__(self, x, y):
        # Инициализация моба
        sprite.Sprite.__init__(self)
        self.image = RIGHT_POSE
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.onGround = False
        self.x_speed = MOVE_SPEED
        self.y_speed = 0

    def update(self, platforms):
        # Изменение позиции моба

        if not self.onGround:
            self.y_speed += GRAVITY

        self.onGround = False

        self.rect.centery += self.y_speed
        self.check_for_collide(0, self.y_speed, platforms)

        self.rect.centerx += self.x_speed
        self.check_for_collide(self.x_speed, 0, platforms)


    def check_for_collide(self, x_speed, y_speed, platforms):
        #Проверка на столкновения с блоками
        for block in platforms:

            if sprite.collide_rect(self, block):

                if x_speed > 0:
                    self.rect.right = block.rect.left
                    self.x_speed = -self.x_speed
                    self.image = LEFT_POSE

                if x_speed < 0:
                    self.rect.left = block.rect.right
                    self.x_speed = -self.x_speed
                    self.image = RIGHT_POSE

                if y_speed > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.y_speed = 0

def update_mobs(mobs, platforms):
    #Обновляем список мобов

    for mob in mobs:
        mob.update(platforms)



