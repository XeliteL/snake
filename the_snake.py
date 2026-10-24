"""Игра «Змейка» на pygame: точка входа."""

import pygame

from controls import handle_keys
from display import clock, draw_pause, screen
from game import check_collisions, eat_apple, eat_poison
from game_objects import Apple, GameObject, Poison, Snake, Stone
from settings import (
    BOARD_BACKGROUND_COLOR, DOWN, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, LEFT,
    RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, UP
)

__all__ = [
    'Apple', 'BOARD_BACKGROUND_COLOR', 'DOWN', 'GRID_HEIGHT', 'GRID_SIZE',
    'GRID_WIDTH', 'GameObject', 'LEFT', 'RIGHT', 'SCREEN_HEIGHT',
    'Poison', 'SCREEN_WIDTH', 'Snake', 'Stone', 'UP', 'clock', 'handle_keys',
    'main', 'screen',
]


def main():
    """Запускает игру и основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple(occupied=snake.positions)
    poison = Poison()
    stone = Stone()
    frame_before_pause = None

    while 1000 - 7:
        clock.tick(snake.speed)

        handle_keys(snake)
        if snake.paused:
            if frame_before_pause is None:
                frame_before_pause = screen.copy()
                draw_pause()
                pygame.display.update()
            continue
        if frame_before_pause is not None:
            screen.blit(frame_before_pause, (0, 0))
            frame_before_pause = None

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            eat_apple(snake, apple, poison, stone)
        elif snake.get_head_position() in poison.positions:
            eat_poison(snake, apple, poison, stone)

        check_collisions(snake, apple, poison, stone)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
