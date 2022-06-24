from pygame import *
import pygame
import sys

left = right = up = down = False

def check_for_events():
    #Обработка событий

    global left, right, up, down
    for event in pygame.event.get():

        #Клик на крестик в правом верхнем углу
        if event.type == QUIT:
            sys.exit()
        #Движение (кнопку нажали)
        elif event.type == KEYDOWN:

            if event.key == K_a or event.key == K_LEFT:
                left = True
            if event.key == K_d or event.key == K_RIGHT:
                right = True
            if event.key == K_SPACE or event.key == K_w:
                up = True
            if event.key == K_s or event.key == K_DOWN:
                down = True

        #Остановка движения (кнопку отпустили)
        elif event.type == KEYUP:

            if event.key == K_a or event.key == K_LEFT:
                left = False
            if event.key == K_d or event.key == K_RIGHT:
                right = False
            if event.key == K_SPACE or event.key == K_w:
                up = False
            if event.key == K_s or event.key == K_DOWN:
                down = False


    #Возвращаем переменные, отвечающие за направление движения или его отсутствие
    return [left, right, up, down]


