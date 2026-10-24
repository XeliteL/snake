"""Игра «Змейка» на pygame: точка входа."""

import pygame

from controls import handle_keys
from display import (
    clock, draw_game_over, draw_pause, draw_victory, screen
)
from game import check_collisions, eat_apple, eat_poison, reset_game
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


def play_frame(snake, apple, poison, stone):
    """Делает один ход: двигает змейку, обрабатывает еду и столкновения.

    Если змейка погибла от отравы, кадр не дорисовывается: рисовать
    уже нечего.
    """
    snake.update_direction()
    snake.move()

    if snake.get_head_position() == apple.position:
        eat_apple(snake, apple, poison, stone)
    elif snake.get_head_position() in poison.positions:
        eat_poison(snake, apple, poison, stone)
        if snake.game_over:
            return

    check_collisions(snake, apple, poison, stone)

    snake.draw()
    apple.draw()
    pygame.display.update()


def main():
    """Запускает игру и основной игровой цикл.

    На паузе, после проигрыша и после победы змейка стоит, а на экране
    висит надпись.
    Когда игрок снимает флаг game_over, игра начинается заново.
    """
    pygame.init()

    snake = Snake()
    apple = Apple(occupied=snake.positions)
    poison = Poison()
    stone = Stone()
    frame_before_pause = None
    game_over_shown = False

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

        if snake.game_over:
            if not game_over_shown:
                game_over_shown = True
                if snake.won:
                    draw_victory()
                else:
                    draw_game_over()
                pygame.display.update()
            continue
        if game_over_shown:
            game_over_shown = False
            reset_game(snake, apple, poison, stone)

        play_frame(snake, apple, poison, stone)


if __name__ == "__main__":
    main()
