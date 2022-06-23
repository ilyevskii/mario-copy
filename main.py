import pygame
from events import check_for_events
from mario import Mario
from platforms import get_sprites, Platform, get_needed_platform
from Mob import update_mobs, Mob

timer = pygame.time.Clock()
BG_WIDTH = 1280
BG_HEIGHT = 720
BG = pygame.image.load("images/background.png")

# Задаем уровень
platforms_coordinates = [
            #x, y, Количество блоков, направление отрисовки
            [0, 0, 32, "hor"],
            [0, 680, 32, "hor"],
            [0, 0, 20, "ver"],
            [200, 300, 7, "hor"],
            [600, 500, 3, "hor"],
            [1160, 400, 3, "hor"],
            [1200, 600, 2, "ver"]
        ]

coins_coordinates = [
        #x, y - координаты монетки
        [360, 640], [625, 460], [250, 260]
]

mobs_coordinates = [
        #x, y - координаты моба
        [650, 450]
]

special_blocks_coordinates = [
        #x, y, Количество блоков, направление отрисовки
        [1000, 550, "mob"]
]

def change_entities(entities, tmp_lst, lst):
    #Функция, удаляющая ненужные спрайты (например, монетка, если ее собрали)
    #tmp_lst - лист спрайтов до сбора монеты, lst - после (т.е. лист без собранной монеты)
    for i in tmp_lst:
        if i not in lst:
            entities.remove(i)

def run():

    pygame.init()
    screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
    pygame.display.set_caption("Anti Mario")
    mario = Mario(50, 50)

    #Создаем списки соответствующих спрайтов и мобов
    platforms = get_sprites(platforms_coordinates, "simple")
    special_platforms = get_sprites(special_blocks_coordinates, "special")
    coins = get_sprites(coins_coordinates, "coins")
    mobs = get_sprites(mobs_coordinates, "mobs")

    #Создаем одну большую группу спрайтов для общей отрисовки
    entities = pygame.sprite.Group()
    entities.add(mario, platforms, mobs, coins, special_platforms)

    while True:

        screen.blit(BG, (0,0))

        # Создаем временные списки монет, мобов и спец.платформ, чтобы отслеживать взаимодействие с ними
        tmp_coins = list(coins)
        tmp_mobs = list(mobs)
        tmp_spec_platforms = list(special_platforms)

        mario.update(check_for_events(), platforms, coins, mobs, special_platforms)
        update_mobs(mobs, platforms)

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
            else:
                mob = None
            block = Platform(x, y)
            platforms.append(block)
            mobs.append(mob)
            entities.add(block, mob)
            change_entities(entities, tmp_spec_platforms, special_platforms)

        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

        #Если жизней нет, очищаем все текстуры. Нужен переход в главное меню
        if int(mario.lives) == 0:
            print("DEAD")
            entities = pygame.sprite.Group()


run()
