"""Игра «Змейка» на pygame: точка входа."""

import pygame

from controls import handle_keys
from game_objects import Apple, GameObject, Snake
from settings import (
    BOARD_BACKGROUND_COLOR, DOWN, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, LEFT,
    RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, UP, clock, screen
)

__all__ = [
    'Apple', 'BOARD_BACKGROUND_COLOR', 'DOWN', 'GRID_HEIGHT', 'GRID_SIZE',
    'GRID_WIDTH', 'GameObject', 'LEFT', 'RIGHT', 'SCREEN_HEIGHT',
    'SCREEN_WIDTH', 'Snake', 'UP', 'clock', 'handle_keys', 'main', 'screen',
]


def main():
    """Запускает игру и основной игровой цикл."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while 1000 - 7:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
