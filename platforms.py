import pygame
from pygame import *
from Mob import Mob
import pyganim

PLATFORM_WIDTH = 40
PLATFORM_HEIGHT = 40
SEWER_WIDTH = 80
SEWER_HEIGHT = 100
COLOR = (0, 0, 0)
ANIMATION_DELAY = 130

COIN_ANIMATION = [("images/coin_0.png"), ("images/coin_1.png"),
              ("images/coin_2.png"), ("images/coin_3.png")]

SPECIAL_BLOCK_ANIMATION = [("images/special_block_0.png"), ("images/special_block_1.png"),
              ("images/special_block_2.png"), ("images/special_block_1.png"), ("images/special_block_0.png")]


class Flour(sprite.Sprite):
    # Базовый класс - кирпич для пола (кирпичный блок)
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        picture = pygame.image.load("images/flour.png")
        picture = pygame.transform.scale(picture, (40, 40))
        self.image = picture

class Platform(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        picture = pygame.image.load("images/block.png")
        picture = pygame.transform.scale(picture, (40, 40))
        self.image = picture


class Stairs(Flour):
    def __init__(self, x, y):
        Flour.__init__(self, x, y)
        picture = pygame.image.load("images/stair.png")
        picture = pygame.transform.scale(picture, (40, 40))
        self.image = picture



class Special_Platform(Flour):
    # Блок с вопросом
    def __init__(self, x, y, type):
        Flour.__init__(self, x, y)
        self.image = image.load("images/special_block.png")
        self.type = type

        # Анимация блока
        boltAnim = []
        for anim in SPECIAL_BLOCK_ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimSpec = pyganim.PygAnimation(boltAnim)
        self.boltAnimSpec.play()

    def update(self):
        self.image.fill(Color(COLOR))
        self.boltAnimSpec.blit(self.image, (0, 0))


class Coin(Flour):
    # Монетка
    def __init__(self, x, y):
        Flour.__init__(self, x, y)
        self.image = image.load("images/special_block.png")
        self.image.set_colorkey(Color(COLOR))

        # Анимация монетки
        boltAnim = []
        for anim in COIN_ANIMATION:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimCoin = pyganim.PygAnimation(boltAnim)
        self.boltAnimCoin.play()

    def update(self):
        self.image.fill(Color(COLOR))
        self.boltAnimCoin.blit(self.image, (0, 0))


class Sewer(Flour):
    # Труба
    def __init__(self, x, y, status):
        Flour.__init__(self, x, y)
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
        if type == "flour" or type == "simple":
            direction = line[3]
            amount = line[2]
        for i in range(amount):

            if type == "flour":
                sprite = Flour(x, y)
            elif type == "simple":
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
                sprite.boltAnimCoin.blit(sprite.image, (0, 0))

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
