import pygame
from pygame import *
from Mob import Mob

PLATFORM_WIDTH = 40
PLATFORM_HEIGHT = 40
SEWER_WIDTH = 80
SEWER_HEIGHT = 100


class Platform(sprite.Sprite):
    # Базовый класс платформа (кирпичный блок)
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        picture = pygame.image.load("images/flour.png")
        picture = pygame.transform.scale(picture, (40, 40))
        self.image = picture


class Stairs(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        picture = pygame.image.load("images/stair.png")
        picture = pygame.transform.scale(picture, (40, 40))
        self.image = picture



class Special_Platform(Platform):
    # Блок с вопросом
    def __init__(self, x, y, type):
        Platform.__init__(self, x, y)
        self.image = image.load("images/special_block.png")
        self.type = type


class Coin(Platform):
    # Монетка
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("images/coin.png")


class Sewer(Platform):
    # Труба
    def __init__(self, x, y, status):
        Platform.__init__(self, x, y)
        self.image = image.load("images/sewer.png")
        self.status = status
        self.rect = Rect(x, y, SEWER_WIDTH, SEWER_HEIGHT)


# class Mushroom(Platform):
#     #грибы
#     def __init__(self, x, y):
#         Platform.__init__(self, x, y)
#         self.image = image.load()

def get_sprites(coordinates, type):
    # Получение структуры уровня
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
            elif type == "sewer":
                sprite = Sewer(x, y, line[2])
            elif type == "stair":
                sprite = Stairs(x, y)
            else:
                sprite = Coin(x, y)

            if direction == "hor":
                x += PLATFORM_WIDTH
            else:
                y += PLATFORM_HEIGHT

            sprites.append(sprite)
    return sprites


def get_needed_platform(temp_blocks, blocks):
    # Функция, которая возвращает даннные о блоке с вопросом, которые активировал игрок
    for i in temp_blocks:
        if i not in blocks:
            return i


def get_status_from_sewer(x, sewers):
    # Функция, возращающая статус трубы - является она телепортом на скрытый уровень или нет. Если является -
    # возвращается номер скрытого уровня

    for i in sewers:
        if i.rect.left < x and i.rect.right > x:
            return i.status
