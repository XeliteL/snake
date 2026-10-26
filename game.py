"""Игровая логика: поедание еды, столкновения и сброс игры."""

from random import randint

from settings import (
    FAST_SPEED,
    FAST_SCORE_STEP,
    FAST_SPEED_STEP,
    GRID_SIZE,
    MAGIC_APPLE_CHANCE,
    MAGIC_SCORE_STEP,
    MAX_SPEED,
    MAX_SCORE_STEP,
    MAX_SPEED_STEP,
    MAX_STONES,
    POISON_EVERY_APPLES,
    POISON_SCORE_STEP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLOW_SCORE_STEP,
    SLOW_SPEED_STEP,
    WIN_LENGTH,
)


def eat_apple(snake, apple, magic_apple, poison, stone):
    """Удлиняет змейку, ускоряет её и добавляет отраву или камни.

    На максимальной скорости с шансом 1 из MAGIC_APPLE_CHANCE появляется
    волшебное яблоко, если его ещё нет на поле.
    Если змейка доросла до WIN_LENGTH, партия выиграна.
    """
    snake.length += 1
    apple.randomize_position(
        snake.positions + stone.positions + poison.positions
        + magic_apple.positions
    )
    if snake.length >= WIN_LENGTH:
        snake.score += MAX_SCORE_STEP
        snake.win()
        return
    if snake.speed < MAX_SPEED:
        if snake.speed < FAST_SPEED:
            snake.speed += SLOW_SPEED_STEP
            snake.score += SLOW_SCORE_STEP
        else:
            snake.speed += FAST_SPEED_STEP
            snake.score += FAST_SCORE_STEP

        if snake.length % POISON_EVERY_APPLES == 0:
            poison.randomize_position(
                snake.positions + stone.positions
                + [apple.position] + magic_apple.positions
            )
    else:
        if (not magic_apple.positions
                and randint(0, MAGIC_APPLE_CHANCE) == MAGIC_APPLE_CHANCE):
            magic_apple.randomize_position(
                snake.positions + stone.positions + poison.positions
                + [apple.position]
            )

        snake.speed += MAX_SPEED_STEP
        snake.score += MAX_SCORE_STEP
        head_x, head_y = snake.get_head_position()
        if len(stone.positions) < MAX_STONES:
            stone.randomize_position(
                snake.positions
                + [apple.position] + poison.positions
                + magic_apple.positions
                + [(x, head_y) for x in range(0, SCREEN_WIDTH, GRID_SIZE)]
                + [(head_x, y) for y in range(0, SCREEN_HEIGHT, GRID_SIZE)]
            )


def reset_game(snake, apple, magic_apple, poison, stone):
    """Возвращает все объекты в начальное состояние."""
    snake.reset()
    stone.reset()
    poison.reset()
    magic_apple.reset()
    apple.randomize_position(snake.positions)


def eat_magic_apple(snake, magic_apple):
    """Начисляет MAGIC_SCORE_STEP очков и убирает волшебное яблоко."""
    snake.score += MAGIC_SCORE_STEP
    magic_apple.reset()


def eat_poison(snake, apple, poison, stone):
    """Укорачивает и замедляет змейку, убирает съеденную отраву.

    Если длина стала нулевой, партия проиграна: поле не трогается,
    его сбросит main() после нажатия клавиши.
    """
    snake.delete_tail()
    snake.speed -= FAST_SPEED_STEP
    snake.score = max(0, snake.score - POISON_SCORE_STEP)
    if snake.length == 0:
        snake.die()
        return
    poison.positions.remove(snake.get_head_position())


def check_collisions(snake, apple, poison, stone):
    """Завершает партию, если змейка врезалась в себя или в камень."""
    if (snake.get_head_position() in snake.positions[1:]
            or snake.get_head_position() in stone.positions):
        snake.die()
