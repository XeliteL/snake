"""Управление змейкой с клавиатуры."""

import pygame

from settings import DOWN, GAME_OVER_DELAY, LEFT, RIGHT, UP


DIRECTION_KEYS = {
    pygame.KSCAN_W: UP,
    pygame.KSCAN_UP: UP,
    pygame.KSCAN_S: DOWN,
    pygame.KSCAN_DOWN: DOWN,
    pygame.KSCAN_A: LEFT,
    pygame.KSCAN_LEFT: LEFT,
    pygame.KSCAN_D: RIGHT,
    pygame.KSCAN_RIGHT: RIGHT,
}


def key_to_direction(event):
    """Возвращает направление для стрелки или WASD, иначе None."""
    return DIRECTION_KEYS.get(event.scancode)


def change_direction(game_object, event):
    """Ставит в очередь поворот по нажатой стрелке или WASD.

    Клавиши определяются по сканкоду, поэтому WASD работает при любой
    раскладке. Развороты на 180 градусов отсекает queue_direction.
    """
    direction = key_to_direction(event)
    if direction:
        game_object.queue_direction(direction)


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
