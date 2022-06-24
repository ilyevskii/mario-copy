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

    def update(self, platforms, sewers):
        # Изменение позиции моба

        if not self.onGround:
            self.y_speed += GRAVITY

        self.onGround = False

        self.rect.centery += self.y_speed
        self.check_for_collide(0, self.y_speed, platforms, sewers)

        self.rect.centerx += self.x_speed
        self.check_for_collide(self.x_speed, 0, platforms, sewers)


    def check_for_collide(self, x_speed, y_speed, platforms, sewers):
        # Проверка на столкновения с блоками
        for block in platforms:
            if sprite.collide_rect(self, block):
                get_collide(self, block, x_speed, y_speed)

        # Проверка на столкновения с трубами
        for sewer in sewers:
            if sprite.collide_rect(self, sewer):
                get_collide(self, sewer, x_speed, y_speed)




def get_collide(mob, block, x_speed, y_speed):
    if x_speed > 0:
        mob.rect.right = block.rect.left
        mob.x_speed = -mob.x_speed
        mob.image = LEFT_POSE

    if x_speed < 0:
        mob.rect.left = block.rect.right
        mob.x_speed = -mob.x_speed
        mob.image = RIGHT_POSE

    if y_speed > 0:
        mob.rect.bottom = block.rect.top
        mob.onGround = True
        mob.y_speed = 0

def update_mobs(mobs, platforms, sewers):
    #Обновляем список мобов

    for mob in mobs:
        mob.update(platforms, sewers)





