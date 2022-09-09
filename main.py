import pygame

from events import check_for_events
from mario import Mario
from platforms import get_sprites, Platform, get_needed_platform, Coin, get_status_from_sewer
from Mob import update_mobs, Mob
from camera import Camera, camera_configure
from menu import *

import random

timer = pygame.time.Clock()
BG_WIDTH = 1280
BG_HEIGHT = 720
screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))


# Задаем уровень
flour_coordinates = [
    [0, 640, 69, "hor"],
    [0, 680, 69, "hor"],
    [0, 0, 30, "ver"],
    [40, 0, 30, "ver"],
    [0, 640, 69, "hor"],
    [0, 680, 69, "hor"],
    [2840, 640, 16, "hor"],
    [2840, 680, 16, "hor"],
    [3600, 640, 109, "hor"],
    [3600, 680, 109, "hor"],
]
platforms_coordinates = [
    #x, y, Количество блоков, направление отрисовки
    [800, 480, 1, "hor"],
    [880, 480, 1, "hor"],
    [960, 480, 1, "hor"],
    [3080, 480, 1, "hor"],
    [3160, 480, 1, "hor"],
    [3760, 480, 1, "hor"],
    [4000, 480, 2, "hor"],
    [3200, 320, 8, "hor"],
    [3640, 320, 3, "hor"],
    [4720, 480, 1, "hor"],
    [4840, 320, 3, "hor"],
    [5080, 320, 1, "hor"],
    [5200, 320, 1, "hor"],
    [5120, 480, 2, "hor"],
    [3440, 280, 1, "hor"],
    [3200, 280, 1, "hor"]

]
stairs_coordinate = [
    [5320, 600], [5360, 600], [5400, 600], [5440, 600],
    [5360, 560], [5400, 560], [5440, 560],
    [5400, 520], [5440, 520],
    [5440, 480],
    [5560, 600], [5600, 600], [5640, 600], [5680, 600],
    [5560, 560], [5600, 560], [5640, 560],
    [5560, 520], [5600, 520],
    [5560, 480],
    [5880, 600], [5920, 600], [5960, 600], [6000, 600], [6040, 600],
    [5920, 560], [5960, 560], [6000, 560], [6040, 560],
    [5960, 520], [6000, 520], [6040, 520],
    [6000, 480], [6040, 480],
    [6160, 600], [6200, 600], [6240, 600], [6280, 600],
    [6160, 560], [6200, 560], [6240, 560],
    [6160, 520], [6200, 520],
    [6160, 480],
    [7160, 600], [7200, 600], [7240, 600], [7280, 600], [7320, 600], [7360, 600], [7400, 600], [7440, 600], [7480, 600],
    [7200, 560], [7240, 560], [7280, 560], [7320, 560], [7360, 560], [7400, 560], [7440, 560], [7480, 560],
    [7240, 520], [7280, 520], [7320, 520], [7360, 520], [7400, 520], [7440, 520], [7480, 520],
    [7280, 480], [7320, 480], [7360, 480], [7400, 480], [7440, 480], [7480, 480],
    [7320, 440], [7360, 440], [7400, 440], [7440, 440], [7480, 440],
    [7360, 400], [7400, 400], [7440, 400], [7480, 400],
    [7400, 360], [7440, 360], [7480, 360],
    [7440, 320], [7480, 320],

]

coins_coordinates = [
    # x, y - координаты монетки
    # [700, 500]
    [550, 580],
    [1100, 500],
    [1350, 580],
    [1450, 580],
    [1650, 580],
    [2050, 500],
    [2790, 480],
    [3250, 480],
    [4100, 580],
    [4200, 580],
    [4300, 580],
    [4600, 480],
    [2450, 580],
    [3080, 420],
    [3250, 200],
    [3300, 200],
    [3350, 200],
    [3400, 200],
    [3700, 260],
    [4030, 420],
    [4850, 260],
    [4900, 260],
    [5500, 580],
    [5500, 530],
    [5500, 480],
    [6100, 580],
    [6100, 530],
    [6100, 480],
    [6680, 580],
    [7000, 580],
    [7470, 100]
]


special_blocks_coordinates = [
    # x, y, тип объекта, который появится (mob или coin)
    [640, 480, "coin"],
    [840, 480, "coin"],
    [920, 480, "coin"],
    [880, 320, "coin"],
    [3120, 480, "coin"],
    [3760, 320, "coin"],
    [4240, 480, "mob"],
    [4360, 480, "coin"],
    [4480, 480, "coin"],
    [5120, 320, "coin"],
    [5160, 320, "coin"],
]

sewer_coordinates = [
    # x, y, номер скрытого уровня в формате "lvl1", "lvl2" (если в трубу нельзя войти - "none")
    [1240, 540, "none", "tube_1"], [1520, 500, "lvl1", "tube_2"],
    [6520, 540, "none", "tube_1"], [2120, 460, "none", "tube_3"], [1800, 460, "none", "tube_3"],
]
# [2120, 460, "none", "tube_3"], [1800, 460, "none", "tube_3"],
mobs_coordinates = [
    # x, y - координаты моба
    [650, 450],
    [880, 450],
    [1780, 450],
    [1841, 450],
    [1680, 450],
    [3320, 280],
    [3360, 280],
    [3960, 450],
    [3920, 450],
    [4960, 450],
    [5000, 450],
    [5120, 410],
    [5160, 370],
    [7120, 450],
    [7160, 450]

]


def change_entities(entities, tmp_lst, lst):
    # Функция, удаляющая ненужные спрайты (например, монетка, если ее собрали)
    # tmp_lst - лист спрайтов до сбора монеты, lst - после (т.е. лист без собранной монеты)
    for i in tmp_lst:
        if i not in lst:
            entities.remove(i)


def run(lives: int):
    mario = Mario(120, 580)
    mario.set_lives(lives)
    pygame.init()
    BG = pygame.image.load("images/background.png")
    pygame.display.set_caption("Anti Mario")

    SCORE = 0

    # Создаем списки соответствующих спрайтов и мобов
    platforms = get_sprites(platforms_coordinates, "simple")
    flours = get_sprites(flour_coordinates, "flour")
    special_platforms = get_sprites(special_blocks_coordinates, "special")
    coins = get_sprites(coins_coordinates, "coins")
    mobs = get_sprites(mobs_coordinates, "mobs")
    sewers = get_sprites(sewer_coordinates, "sewer")
    stairs = get_sprites(stairs_coordinate, "stair")

    # Создаем одну большую группу спрайтов для общей отрисовки
    entities = pygame.sprite.Group()
    animatedEntities = pygame.sprite.Group()
    entities.add(mario, platforms, mobs, coins, special_platforms, sewers, stairs, flours)
    animatedEntities.add(coins, special_platforms)

    # Создание камеры
    total_level_width = BG_WIDTH ** 2 / 40
    total_level_height = BG_HEIGHT ** 2 / 40

    camera = Camera(camera_configure, total_level_width, total_level_height)
    status = "Running"

    pygame.mixer.music.load('music/play_background_music.mp3')
    pygame.mixer.music.play(-1)

    count = 0

    max_coordinate = 0
    score = 0

    while status == "Running":

        if max_coordinate < int(mario.rect.x / 120 - 1):
            dif = int(mario.rect.x / 120 - 1) - max_coordinate
            max_coordinate = int(mario.rect.x / 120 - 1)
            score += dif

        screen.blit(BG, (0, 0))

        # Создаем временные списки монет, мобов и спец.платформ, чтобы отслеживать взаимодействие с ними
        tmp_coins = list(coins)
        tmp_mobs = list(mobs)
        tmp_spec_platforms = list(special_platforms)

        events = check_for_events(pause=game_pause, screen=screen, run=run)
        if events[3]:
            if mario.onTube:
                tmp_status = get_status_from_sewer(mario.rect.centerx, sewers)
                if tmp_status != "none":
                    status = tmp_status

        if mario.update(events, platforms, coins, mobs, special_platforms, sewers, stairs, flours) is True:
            death_sound = pygame.mixer.Sound('music/death.wav')
            death_sound.play(0)
            mario.set_position(120, 300)
            mario.set_x_speed(0)
            mario.set_y_speed(0)

        update_mobs(mobs, platforms, sewers, stairs, flours)

        # При взаимодействии например, с монетой, mario.update() из списка coins удаляется монета, с которой
        # взаимодействовали. В списке tmp_coins эта монета ещё есть. В ифе удаляем монету из спрайтов
        if len(tmp_coins) != len(coins):
            coin_sound = pygame.mixer.Sound('music/coin.wav')
            coin_sound.play(0)
            change_entities(entities, tmp_coins, coins)
            count += 1

        if len(tmp_mobs) != len(mobs):
            mob_sound = pygame.mixer.Sound('music/mob_dead.wav')
            mob_sound.play(0)
            change_entities(entities, tmp_mobs, mobs)
            score += 25

        COIN_TEXT = get_font(20).render(f"COIN COUNT: {count}", True, "Yellow")
        COIN_RECT = COIN_TEXT.get_rect(center=(1090, 50))
        screen.blit(COIN_TEXT, COIN_RECT)

        LIVES_TEXT = get_font(20).render(f"LIVES: {mario.lives}", True, "Black")
        LIVES_RECT = LIVES_TEXT.get_rect(center=(1140, 90))
        screen.blit(LIVES_TEXT, LIVES_RECT)

        LIVES_TEXT = get_font(20).render(f"SCORE: {mario.rect.x}  {mario.rect.y}", True, "Black")
        LIVES_RECT = LIVES_TEXT.get_rect(center=(800, 130))
        screen.blit(LIVES_TEXT, LIVES_RECT)

        if mario.rect.x > 7700:
            status = 'win'
            break

        # Если врезались в блок с вопросом. Получаем нужный блок, его координаты. Меняем блок с вопросиком на обычный
        # блок. На блок ставим монету или моба, в зависимости от типа, который передается при конструировании уровня
        if len(tmp_spec_platforms) != len(special_platforms):
            special_sound = pygame.mixer.Sound('music/special_sound.wav')
            special_sound.play(0)
            block = get_needed_platform(tmp_spec_platforms, special_platforms)
            x = block.rect.x
            y = block.rect.y
            mob = None
            if block.type == "mob":
                mob = Mob(x, y - 40)
                mobs.append(mob)
            elif block.type == "coin":
                mob = Coin(x, y - 45)
                coins.append(mob)
                animatedEntities.add(mob)

            block = Platform(x, y)
            platforms.append(block)
            entities.add(block, mob)
            change_entities(entities, tmp_spec_platforms, special_platforms)

        camera.update(mario)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        COIN_TEXT = get_font(20).render(f"COIN COUNT: {count}", True, "Yellow")
        COIN_RECT = COIN_TEXT.get_rect(center=(1090, 50))
        screen.blit(COIN_TEXT, COIN_RECT)

        LIVES_TEXT = get_font(20).render(f"LIVES: {mario.lives}", True, "Red")
        LIVES_RECT = LIVES_TEXT.get_rect(center=(1140, 90))
        screen.blit(LIVES_TEXT, LIVES_RECT)

        LIVES_TEXT = get_font(20).render(f"SCORE: {score}", True, "Black")
        LIVES_RECT = LIVES_TEXT.get_rect(center=(1140, 130))
        screen.blit(LIVES_TEXT, LIVES_RECT)

        pygame.display.update()
        animatedEntities.update()
        timer.tick(60)

        # Если жизней нет, очищаем все текстуры. Нужен переход в главное меню
        if int(mario.lives) == 0:
            status = "dead"
            break

    return status, score, count


main_menu(screen=screen, run=run)
