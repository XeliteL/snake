"""Тесты игровых объектов и логики из game.py."""

import pygame
import pytest

from game import check_collisions, eat_apple, eat_poison, reset_game
from game_objects import Apple, Poison, Snake, Stone
from settings import (
    GRID_SIZE, LEFT, RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, START_SPEED, UP,
    WIN_LENGTH
)

ALL_CELLS = [
    (x, y)
    for x in range(0, SCREEN_WIDTH, GRID_SIZE)
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
]
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Сколько раз повторять проверки со случайными клетками.
REPEATS = 200
# Время проигрыша, которое возвращает подменённый pygame.time.get_ticks.
NOW = 12345


@pytest.fixture
def frozen_ticks(monkeypatch):
    """Подменяет текущее время pygame на NOW."""
    monkeypatch.setattr(pygame.time, 'get_ticks', lambda: NOW)


@pytest.fixture
def objects():
    """Змейка, яблоко, отрава и камни в начальном состоянии."""
    snake = Snake()
    return snake, Apple(occupied=snake.positions), Poison(), Stone()


# --- Еда и камни: выбор клетки ---

def test_food_picks_only_free_cell():
    free = (100, 100)
    occupied = [cell for cell in ALL_CELLS if cell != free]
    apple = Apple(occupied=occupied)
    assert apple.position == free
    assert apple.randomize_position(occupied) == free


def test_food_position_is_on_grid():
    apple = Apple()
    for _ in range(REPEATS):
        assert apple.randomize_position() in ALL_CELLS


def test_poison_starts_empty_and_resets():
    poison = Poison()
    assert poison.positions == []
    cell = poison.randomize_position()
    assert poison.positions == [cell]
    poison.reset()
    assert poison.positions == []


def test_full_field_does_not_hang():
    apple, poison, stone = Apple(), Poison(), Stone()
    position = apple.position
    assert apple.randomize_position(ALL_CELLS) == position
    assert poison.randomize_position(ALL_CELLS) is None
    assert poison.positions == []
    stone.randomize_position(ALL_CELLS)
    assert stone.positions == []


def test_poison_and_stone_skip_occupied():
    free = (40, 60)
    occupied = [cell for cell in ALL_CELLS if cell != free]
    poison, stone = Poison(), Stone()
    assert poison.randomize_position(occupied) == free
    stone.randomize_position(occupied)
    assert stone.positions == [free]
    stone.reset()
    assert stone.positions == []


# --- Змейка ---

def test_snake_moves_and_wraps_around_edges():
    snake = Snake(positions=[(SCREEN_WIDTH - GRID_SIZE, 0)], direction=RIGHT)
    snake.move()
    assert snake.get_head_position() == (0, 0)
    snake.direction = UP
    snake.move()
    assert snake.get_head_position() == (0, SCREEN_HEIGHT - GRID_SIZE)


def test_snake_reset_restores_start_state():
    snake = Snake()
    snake.length = 5
    snake.speed = 20
    snake.direction = LEFT
    snake.direction_queue = [UP]
    snake.paused = True
    snake.game_over = True
    snake.game_over_time = NOW
    snake.reset()
    assert snake.length == 1
    assert snake.positions == [CENTER]
    assert snake.speed == START_SPEED
    assert snake.direction == RIGHT
    assert snake.direction_queue == []
    assert not snake.paused
    assert not snake.game_over
    assert snake.game_over_time == 0



@pytest.mark.usefixtures('frozen_ticks')
def test_snake_die_ends_game_and_remembers_time():
    snake = Snake()
    snake.die()
    assert snake.game_over
    assert snake.game_over_time == NOW

# --- eat_apple ---

def test_eat_apple_grows_and_speeds_up(objects):
    snake, apple, poison, stone = objects
    eat_apple(snake, apple, poison, stone)
    assert snake.length == 2
    assert snake.speed == START_SPEED + 0.5
    assert apple.position not in snake.positions


def test_speed_never_drops_on_apple(objects):
    snake, apple, poison, stone = objects
    # До победы: на WIN_LENGTH змейка выигрывает и больше не ускоряется.
    for _ in range(WIN_LENGTH - 2):
        speed = snake.speed
        eat_apple(snake, apple, poison, stone)
        assert snake.speed > speed


def test_eat_apple_adds_poison_every_ten(objects):
    snake, apple, poison, stone = objects
    snake.length = 8
    eat_apple(snake, apple, poison, stone)
    assert poison.positions == []
    eat_apple(snake, apple, poison, stone)
    assert len(poison.positions) == 1
    assert poison.positions[0] not in snake.positions + [apple.position]


def test_eat_apple_adds_stone_at_max_speed(objects):
    snake, apple, poison, stone = objects
    snake.speed = 25
    eat_apple(snake, apple, poison, stone)
    assert len(stone.positions) == 1
    assert snake.speed == pytest.approx(25.1)


def test_stone_never_in_head_row_or_column(objects):
    snake, apple, poison, stone = objects
    snake.speed = 25
    head_x, head_y = snake.get_head_position()
    for _ in range(REPEATS):
        eat_apple(snake, apple, poison, stone)
        x, y = stone.positions[-1]
        assert x != head_x and y != head_y
        stone.reset()
        snake.length = 1


# --- eat_poison ---

def test_eat_poison_removes_only_eaten_one(objects):
    snake, apple, poison, stone = objects
    snake.length = 3
    snake.positions = [CENTER, (300, 240), (280, 240)]
    poison.positions = [CENTER, (0, 0)]
    eat_poison(snake, apple, poison, stone)
    assert snake.length == 2
    assert poison.positions == [(0, 0)]


@pytest.mark.usefixtures('frozen_ticks')
def test_eat_poison_at_length_one_ends_game(objects):
    snake, apple, poison, stone = objects
    snake.positions = [(0, 0)]
    poison.positions = [(0, 0), (40, 40)]
    stone.positions = [(100, 100)]
    eat_poison(snake, apple, poison, stone)
    assert snake.game_over
    assert snake.game_over_time == NOW
    # Поле не сбрасывается: это сделает main() после нажатия клавиши.
    assert snake.length == 0
    assert poison.positions == [(0, 0), (40, 40)]
    assert stone.positions == [(100, 100)]


def test_eat_poison_keeps_game_while_snake_is_long(objects):
    snake, apple, poison, stone = objects
    snake.length = 2
    snake.positions = [CENTER, (300, 240)]
    poison.positions = [CENTER]
    eat_poison(snake, apple, poison, stone)
    assert not snake.game_over


def test_eat_poison_shortens_body(objects):
    snake, apple, poison, stone = objects
    snake.length = 4
    snake.positions = [CENTER, (300, 240), (280, 240), (260, 240)]
    poison.positions = [CENTER]
    eat_poison(snake, apple, poison, stone)
    snake.move()
    assert len(snake.positions) == snake.length == 3


# --- Столкновения и сброс ---

def test_no_collision_keeps_game(objects):
    snake, apple, poison, stone = objects
    snake.length = 3
    stone.positions = [(0, 0)]
    check_collisions(snake, apple, poison, stone)
    assert snake.length == 3
    assert stone.positions == [(0, 0)]
    assert not snake.game_over


@pytest.mark.usefixtures('frozen_ticks')
def test_collision_with_self_ends_game(objects):
    snake, apple, poison, stone = objects
    snake.length = 4
    snake.positions = [(0, 0), (20, 0), (0, 0)]
    poison.positions = [(40, 40)]
    check_collisions(snake, apple, poison, stone)
    assert snake.game_over
    assert snake.game_over_time == NOW
    assert snake.length == 4
    assert poison.positions == [(40, 40)]


@pytest.mark.usefixtures('frozen_ticks')
def test_collision_with_stone_ends_game(objects):
    snake, apple, poison, stone = objects
    snake.length = 4
    stone.positions = [CENTER]
    check_collisions(snake, apple, poison, stone)
    assert snake.game_over
    assert snake.game_over_time == NOW
    assert snake.length == 4
    assert stone.positions == [CENTER]


def test_reset_game_moves_apple_off_snake(objects):
    snake, apple, poison, stone = objects
    for _ in range(REPEATS):
        apple.position = CENTER
        reset_game(snake, apple, poison, stone)
        assert apple.position != CENTER
