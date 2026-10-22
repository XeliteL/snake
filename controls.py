"""Управление змейкой с клавиатуры."""

import pygame

from settings import DOWN, LEFT, RIGHT, UP


def handle_keys(game_object):
    """Обрабатывает события: закрытие окна и нажатия стрелок или WASD.

    Клавиши определяются по сканкоду, поэтому WASD работает при любой
    раскладке. Запрещает разворот змейки на 180 градусов.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.scancode in (pygame.KSCAN_W, pygame.KSCAN_UP)
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif (event.scancode in (pygame.KSCAN_S, pygame.KSCAN_DOWN)
                    and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.scancode in (pygame.KSCAN_A, pygame.KSCAN_LEFT)
                    and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.scancode in (pygame.KSCAN_D, pygame.KSCAN_RIGHT)
                    and game_object.direction != LEFT):
                game_object.next_direction = RIGHT
