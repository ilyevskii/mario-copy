import pygame, sys
from button import Button


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def game_over(screen, run, score: int, coins: int):
    pygame.mixer.music.load('music/mario-dead.mp3')
    pygame.mixer.music.play(1)


    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        PLAY_TEXT = get_font(90).render("GAME OVER!", True, "Red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(660, 150))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        SCORE_TEXT = get_font(45).render(f"Your score {score}", True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(660, 270))
        screen.blit(SCORE_TEXT, SCORE_RECT)

        COIN_TEXT = get_font(45).render(f"Coins {coins}", True, "Yellow")
        COIN_RECT = COIN_TEXT.get_rect(center=(660, 360))
        screen.blit(COIN_TEXT, COIN_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 520),
                            text_input="GO TO MENU", font=get_font(75), base_color="White", hovering_color="Orange")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.load('music/menu_background_music.mp3')
                    main_menu(screen, run)

        pygame.display.update()


def win(screen, run, score: int, coins: int):
    pygame.mixer.music.load('music/win.wav')
    pygame.mixer.music.play(1)


    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        PLAY_TEXT = get_font(90).render("YOU WIN!", True, "Green")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(660, 150))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        SCORE_TEXT = get_font(45).render(f"Your score {score}", True, "Blue")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(660, 270))
        screen.blit(SCORE_TEXT, SCORE_RECT)

        COIN_TEXT = get_font(45).render(f"Coins {coins}", True, "Yellow")
        COIN_RECT = COIN_TEXT.get_rect(center=(660, 360))
        screen.blit(COIN_TEXT, COIN_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 520),
                            text_input="GO TO MENU", font=get_font(75), base_color="Black", hovering_color="Red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.load('music/menu_background_music.mp3')
                    main_menu(screen, run)

        pygame.display.update()


def game_pause(screen, run):
    pygame.mixer.music.pause()
    coin_sound = pygame.mixer.Sound('music/pause.wav')
    coin_sound.play(0)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("White")

        PLAY_TEXT = get_font(90).render("Game is pause", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        CONTINUE_PLAY = Button(image=None, pos=(640, 450),
                            text_input="CONTINUE", font=get_font(75), base_color="Black", hovering_color="Green")

        MENU = Button(image=None, pos=(640, 600),
                            text_input="MENU", font=get_font(75), base_color="Black", hovering_color="Red")

        CONTINUE_PLAY.changeColor(PLAY_MOUSE_POS)
        CONTINUE_PLAY.update(screen)

        MENU.changeColor(PLAY_MOUSE_POS)
        MENU.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_PLAY.checkForInput(PLAY_MOUSE_POS):
                    pygame.mixer.music.unpause()

                    return
                if MENU.checkForInput(PLAY_MOUSE_POS):
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.load('music/menu_background_music.mp3')
                    main_menu(screen, run)

        pygame.display.update()


def options(screen, run):


    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("Powered by:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 130))

        ILYA = get_font(45).render('Ilya Andreevskii', True, "Black")
        ILYA_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))

        PAVEL = get_font(45).render('Pavel Glytov', True, "Black")
        PAVEL_RECT = OPTIONS_TEXT.get_rect(center=(580, 360))

        ANDREW = get_font(45).render('Andrew Logvinov', True, "Black")
        ANDREW_RECT = OPTIONS_TEXT.get_rect(center=(530, 460))

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

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('music/menu_background_music.mp3')
        pygame.mixer.music.play(-1)

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

                    params = run(5, 0)
                    if params[0] == 'dead':
                        game_over(screen, run, score=params[1], coins=params[2])

                    elif params[0] == 'win':
                        win(screen, run, score=params[1], coins=params[2])

                    elif params[0] == 'lvl1':
                        params = run(5, 1)

                        if params[0] == 'dead':
                            game_over(screen, run, score=params[1], coins=params[2])
                        elif params[0] == "lvl2":

                            params = run(5, 2)
                            if params[0] == 'dead':
                                game_over(screen, run, score=params[1], coins=params[2])

                            elif params[0] == 'win':
                                win(screen, run, score=params[1], coins=params[2])

                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(screen, run)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
