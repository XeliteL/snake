"""Игровая логика: поедание еды, столкновения и сброс игры."""

from settings import (
    FAST_SPEED,
    FAST_SCORE_STEP,
    FAST_SPEED_STEP,
    GRID_SIZE,
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


def eat_apple(snake, apple, poison, stone):
    """Удлиняет змейку, ускоряет её и добавляет отраву или камни.

    Если змейка доросла до WIN_LENGTH, партия выиграна.
    """
    snake.length += 1
    if snake.length >= WIN_LENGTH:
        snake.score += MAX_SCORE_STEP
        snake.win()
        return
    apple.randomize_position(
        snake.positions + stone.positions + poison.positions
    )
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
                + [apple.position]
            )
    else:
        snake.speed += MAX_SPEED_STEP
        snake.score += MAX_SCORE_STEP
        head_x, head_y = snake.get_head_position()
        if len(stone.positions) < MAX_STONES:
            stone.randomize_position(
                snake.positions
                + [apple.position] + poison.positions
                + [(x, head_y) for x in range(0, SCREEN_WIDTH, GRID_SIZE)]
                + [(head_x, y) for y in range(0, SCREEN_HEIGHT, GRID_SIZE)]
            )


def reset_game(snake, apple, poison, stone):
    """Возвращает все объекты в начальное состояние."""
    snake.reset()
    stone.reset()
    poison.reset()
    apple.randomize_position(snake.positions)


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
