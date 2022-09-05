import pygame, sys
from button import Button


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def game_over(screen, run):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        PLAY_TEXT = get_font(90).render("GAME OVER!", True, "Red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(660, 260))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="GO TO MENU", font=get_font(75), base_color="White", hovering_color="Red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(screen, run)

        pygame.display.update()


def options(screen, run):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("Powerd by:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 130))

        ILYA = get_font(45).render('Ilya Andreevskii', True, "Black")
        ILYA_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))

        PAVEL = get_font(45).render('Pavel Glytov', True, "Black")
        PAVEL_RECT = OPTIONS_TEXT.get_rect(center=(580, 360))

        ANDREW = get_font(45).render('Andrew Logvinov', True, "Black")
        ANDREW_RECT = OPTIONS_TEXT.get_rect(center=(340, 460))

        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        screen.blit(ILYA, ILYA_RECT)
        screen.blit(PAVEL, PAVEL_RECT)
        screen.blit(ANDREW, ANDREW_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 600),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(screen, run)

        pygame.display.update()


def main_menu(screen, run):
    pygame.init()
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("assets/Background.png")

    get_continued = True

    while get_continued:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    status = run()
                    if status == 'dead':
                        game_over(screen, run)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(screen, run)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
