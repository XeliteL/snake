"""Игра «Змейка» на pygame: точка входа."""

import pygame

from controls import handle_keys
from display import (
    clock, draw_game_over, draw_pause, draw_victory, screen, init_display,
    copy_screen, format_score
)
from game import check_collisions, eat_apple, eat_poison, reset_game
from game_objects import Apple, GameObject, Poison, Snake, Stone
from record import load_record, save_record
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


def play_frame(snake, apple, poison, stone, record):
    """Делает один ход: двигает змейку, обрабатывает еду и столкновения.

    Кадр каждый раз рисуется заново: экран заливается фоном, затем
    рисуются все объекты. Если змейка погибла от отравы, кадр не
    перерисовывается: рисовать уже нечего.
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

    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()
    apple.draw()
    poison.draw()
    stone.draw()
    copy_screen()
    pygame.display.set_caption(format_score(snake.score, record))


def main():
    """Запускает игру и основной игровой цикл.

    На паузе, после проигрыша и после победы змейка стоит, а на экране
    висит надпись.
    Когда игрок снимает флаг game_over, игра начинается заново.
    """
    pygame.init()
    init_display()

    snake = Snake()
    apple = Apple(occupied=snake.positions)
    poison = Poison()
    stone = Stone()
    pause_shown = False
    game_over_shown = False
    record = load_record()

    while 1000 - 7:
        clock.tick(snake.speed)

        handle_keys(snake)
        if snake.paused:
            if not pause_shown:
                pause_shown = True
                draw_pause()
                copy_screen()
            continue
        pause_shown = False

        if snake.game_over:
            if not game_over_shown:
                game_over_shown = True
                if snake.score > record:
                    record = snake.score
                    save_record(record)
                if snake.won:
                    draw_victory(snake.score, record)
                else:
                    draw_game_over(snake.score, record)
                copy_screen()
            continue
        if game_over_shown:
            game_over_shown = False
            reset_game(snake, apple, poison, stone)

        play_frame(snake, apple, poison, stone, record)


if __name__ == "__main__":
    main()
