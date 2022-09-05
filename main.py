import pygame
from events import check_for_events
from mario import Mario
from platforms import get_sprites, Platform, get_needed_platform, Coin, get_status_from_sewer
from Mob import update_mobs, Mob
from camera import Camera, camera_configure

timer = pygame.time.Clock()
BG_WIDTH = 1280
BG_HEIGHT = 720
BG = pygame.image.load("images/background.png")

# Задаем уровень
# platforms_coordinates = [
#             #x, y, Количество блоков, направление отрисовки
#             [0, 0, 64, "hor"],
#             [0, 680, 64, "hor"],
#             [0, 0, 20, "ver"],
#             [2520, 0, 20, "ver"],
#             [200, 300, 7, "hor"],
#             [600, 500, 3, "hor"],
#             [1160, 400, 3, "hor"],
#             [1200, 600, 2, "ver"]
# ]
platforms_coordinates = [
    [0, 640, 69, "hor"],
    [0, 680, 69, "hor"],
    [2840, 640, 16, "hor"],
    [2840, 680, 16, "hor"],
    [3600, 640, 109, "hor"],
    [3600, 680, 109, "hor"],
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
    [4960, 320, 2, "hor"]

]

coins_coordinates = [
    # x, y - координаты монетки
    [360, 640], [625, 460], [250, 260]
]

mobs_coordinates = [
    # x, y - координаты моба
    [650, 450]
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
    [4480, 480, "coin"]
]

sewer_coordinates = [
    # x, y, номер скрытого уровня в формате "lvl1", "lvl2" (если в трубу нельзя войти - "none")
    [400, 600, "none"], [1700, 580, "lvl1"]
]


def change_entities(entities, tmp_lst, lst):
    # Функция, удаляющая ненужные спрайты (например, монетка, если ее собрали)
    # tmp_lst - лист спрайтов до сбора монеты, lst - после (т.е. лист без собранной монеты)
    for i in tmp_lst:
        if i not in lst:
            entities.remove(i)


def run():
    pygame.init()
    screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
    pygame.display.set_caption("Anti Mario")
    mario = Mario(50, 50)

    # Создаем списки соответствующих спрайтов и мобов
    platforms = get_sprites(platforms_coordinates, "simple")
    special_platforms = get_sprites(special_blocks_coordinates, "special")
    coins = get_sprites(coins_coordinates, "coins")
    mobs = get_sprites(mobs_coordinates, "mobs")
    sewers = get_sprites(sewer_coordinates, "sewer")

    # Создаем одну большую группу спрайтов для общей отрисовки
    entities = pygame.sprite.Group()
    entities.add(mario, platforms, mobs, coins, special_platforms, sewers)

    # Создание камеры
    total_level_width = BG_WIDTH ** 2 / 40
    total_level_height = BG_HEIGHT ** 2 / 40

    camera = Camera(camera_configure, total_level_width, total_level_height)
    status = "Running"

    while status == "Running":

        screen.blit(BG, (0, 0))

        # Создаем временные списки монет, мобов и спец.платформ, чтобы отслеживать взаимодействие с ними
        tmp_coins = list(coins)
        tmp_mobs = list(mobs)
        tmp_spec_platforms = list(special_platforms)

        events = check_for_events()
        if events[3]:
            if mario.onTube:
                tmp_status = get_status_from_sewer(mario.rect.centerx, sewers)
                if tmp_status != "none":
                    status = tmp_status

        mario.update(events, platforms, coins, mobs, special_platforms, sewers)
        update_mobs(mobs, platforms, sewers)

        # При взаимодействии например, с монетой, mario.update() из списка coins удаляется монета, с которой
        # взаимодействовали. В списке tmp_coins эта монета ещё есть. В ифе удаляем монету из спрайтов
        if len(tmp_coins) != len(coins):
            change_entities(entities, tmp_coins, coins)

        if len(tmp_mobs) != len(mobs):
            change_entities(entities, tmp_mobs, mobs)

        # Если врезались в блок с вопросом. Получаем нужный блок, его координаты. Меняем блок с вопросиком на обычный
        # блок. На блок ставим монету или моба, в зависимости от типа, который передается при конструировании уровня
        if len(tmp_spec_platforms) != len(special_platforms):
            block = get_needed_platform(tmp_spec_platforms, special_platforms)
            x = block.rect.x
            y = block.rect.y
            if block.type == "mob":
                mob = Mob(x, y - 40)
            elif block.type == "coin":
                mob = Coin(x, y - 40)
            else:
                mob = None
            block = Platform(x, y)
            platforms.append(block)
            mobs.append(mob)
            entities.add(block, mob)
            change_entities(entities, tmp_spec_platforms, special_platforms)

        camera.update(mario)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()
        timer.tick(60)

        # Если жизней нет, очищаем все текстуры. Нужен переход в главное меню
        if int(mario.lives) == 0:
            status = "dead"

    return status


status = run()
if status == "lvl1":
    print("lvl1")
elif status == "dead":
    print("dead")
