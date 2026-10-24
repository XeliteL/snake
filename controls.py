"""Управление змейкой с клавиатуры."""

import pygame

from settings import DOWN, GAME_OVER_DELAY, LEFT, RIGHT, UP


def change_direction(game_object, event):
    """Выбирает новое направление по нажатой стрелке или WASD.

    Клавиши определяются по сканкоду, поэтому WASD работает при любой
    раскладке. Запрещает разворот змейки на 180 градусов.
    """
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


def handle_keys(game_object):
    """Обрабатывает события: закрытие окна, проигрыш, пауза и движение.

    После проигрыша любая клавиша снимает флаг game_over, но только
    когда прошло GAME_OVER_DELAY миллисекунд; более ранние нажатия
    игнорируются. P или Esc ставят игру на паузу и снимают с неё;
    на паузе стрелки и WASD игнорируются. Остальные нажатия передаются
    в change_direction.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if game_object.game_over:
                if (pygame.time.get_ticks() - game_object.game_over_time
                        >= GAME_OVER_DELAY):
                    game_object.game_over = False
            elif event.scancode in (pygame.KSCAN_P, pygame.KSCAN_ESCAPE):
                game_object.paused = not game_object.paused
            elif game_object.paused:
                continue
            else:
                change_direction(game_object, event)
