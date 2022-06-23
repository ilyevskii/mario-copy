from pygame import *
from Mob import Mob

PLATFORM_WIDTH = 40
PLATFORM_HEIGHT = 40

class Platform(sprite.Sprite):
    #Базовый класс платформа (кирпичный блок)
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("images/block.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Special_Platform(Platform):
    #Блок с вопросом
    def __init__(self, x, y, type):
        Platform.__init__(self, x, y)
        self.image = image.load("images/special_block.png")
        self.type = type
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

class Coin(Platform):
    #Монетка
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("images/coin.png")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)



def get_sprites(coordinates, type):
    #Получение структуры уровня
    amount = 1
    direction = "ver"

    sprites = []
    for line in coordinates:
        x = line[0]
        y = line[1]

        # По умолчанию отрисовывается один блок по вертикали. Но если coordinates - это список обычных кирпичных блоков,
        # там значения количества рисуемых блоков и направление отрисовки могут быть иными. Поэтому достаем amount
        # и direction из списка
        if type == "simple":
            direction = line[3]
            amount = line[2]
        for i in range(amount):

            if type == "simple":
                sprite = Platform(x, y)
            elif type == "special":
                sprite = Special_Platform(x, y, line[2])
            elif type == "mobs":
                sprite = Mob(x, y)
            else:
                sprite = Coin(x, y)

            if direction == "hor":
                x += PLATFORM_WIDTH
            else:
                y += PLATFORM_HEIGHT

            sprites.append(sprite)
    return sprites

def get_needed_platform(temp_blocks, blocks):
    #Функция, которая возвращает даннные о блоке с вопросом, которые активировал игрок
    for i in temp_blocks:
        if i not in blocks:
            return i