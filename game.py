"""Игровая логика: поедание еды и столкновения."""

from settings import (
    FAST_SPEED,
    FAST_SPEED_STEP,
    GRID_SIZE,
    MAX_SPEED,
    MAX_SPEED_STEP,
    POISON_EVERY_APPLES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLOW_SPEED_STEP,
)


def eat_apple(snake, apple, poison, stone):
    """Удлиняет змейку, ускоряет её и добавляет отраву или камни."""
    snake.length += 1
    apple.randomize_position(
        snake.positions + stone.positions + poison.positions
    )
    if snake.speed < MAX_SPEED:
        if snake.speed < FAST_SPEED:
            snake.speed += SLOW_SPEED_STEP
        else:
            snake.speed += FAST_SPEED_STEP

        if snake.length % POISON_EVERY_APPLES == 0:
            poison.randomize_position(
                snake.positions + stone.positions
                + [snake.last, apple.position]
            )
            poison.draw()
    else:
        snake.speed += MAX_SPEED_STEP
        head_x, head_y = snake.get_head_position()
        stone.randomize_position(
            snake.positions
            + [snake.last, apple.position] + poison.positions
            + [(x, head_y) for x in range(0, SCREEN_WIDTH, GRID_SIZE)]
            + [(head_x, y) for y in range(0, SCREEN_HEIGHT, GRID_SIZE)]
        )
        stone.draw()


def reset_game(snake, apple, poison, stone):
    """Возвращает все объекты в начальное состояние."""
    snake.reset()
    stone.reset()
    poison.reset()
    apple.randomize_position(snake.positions)


def eat_poison(snake, apple, poison, stone):
    """Укорачивает змейку; если длина стала нулевой — сбрасывает игру."""
    snake.delete_tail()
    if snake.length == 0:
        reset_game(snake, apple, poison, stone)
        return
    poison.positions.remove(snake.get_head_position())


def check_collisions(snake, apple, poison, stone):
    """Сбрасывает игру, если змейка врезалась в себя или в камень."""
    if (snake.get_head_position() in snake.positions[1:]
            or snake.get_head_position() in stone.positions):
        reset_game(snake, apple, poison, stone)
