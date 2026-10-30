"""Тесты управления змейкой из controls.py."""

import pygame
import pytest

from controls import handle_keys
from game_objects import Snake
from settings import (
    BOOST_MULTIPLIER, DOWN, GAME_OVER_DELAY, LEFT, MAX_BOOST_SPEED,
    MAX_QUEUED_TURNS, RIGHT, UP,
)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
KEYS = [
    (pygame.KSCAN_UP, UP),
    (pygame.KSCAN_W, UP),
    (pygame.KSCAN_DOWN, DOWN),
    (pygame.KSCAN_S, DOWN),
    (pygame.KSCAN_LEFT, LEFT),
    (pygame.KSCAN_A, LEFT),
    (pygame.KSCAN_RIGHT, RIGHT),
    (pygame.KSCAN_D, RIGHT),
]
KEY_NAMES = ['up', 'w', 'down', 's', 'left', 'a', 'right', 'd']


def press(monkeypatch, *events):
    """Подменяет очередь событий pygame на переданные события."""
    monkeypatch.setattr(pygame.event, 'get', lambda: list(events))


def key_event(scancode, key=0):
    """Создаёт событие нажатия клавиши с заданным сканкодом."""
    return pygame.event.Event(pygame.KEYDOWN, scancode=scancode, key=key)


def key_up_event(scancode, key=0):
    """Создаёт событие отпускания клавиши с заданным сканкодом."""
    return pygame.event.Event(pygame.KEYUP, scancode=scancode, key=key)


def snake_moving(direction):
    """Создаёт змейку, которая движется в заданном направлении."""
    snake = Snake()
    snake.direction = direction
    return snake


@pytest.mark.parametrize('scancode, direction', KEYS, ids=KEY_NAMES)
def test_key_sets_direction(monkeypatch, scancode, direction):
    # Двигаемся перпендикулярно, чтобы поворот был разрешён.
    start = LEFT if direction in (UP, DOWN) else UP
    snake = snake_moving(start)
    press(monkeypatch, key_event(scancode))
    handle_keys(snake)
    assert snake.direction_queue == [direction]


@pytest.mark.parametrize('scancode, direction', KEYS, ids=KEY_NAMES)
def test_reverse_is_blocked(monkeypatch, scancode, direction):
    snake = snake_moving(OPPOSITE[direction])
    press(monkeypatch, key_event(scancode))
    handle_keys(snake)
    assert snake.direction_queue == []


def test_wasd_works_with_russian_layout(monkeypatch):
    snake = snake_moving(LEFT)
    # Физическая W при русской раскладке даёт символ «ц».
    press(monkeypatch, key_event(pygame.KSCAN_W, key=ord('ц')))
    handle_keys(snake)
    assert snake.direction_queue == [UP]


def test_other_keys_are_ignored(monkeypatch):
    snake = snake_moving(RIGHT)
    press(monkeypatch, key_event(pygame.KSCAN_SPACE))
    handle_keys(snake)
    assert snake.direction_queue == []
    assert snake.direction == RIGHT


def test_quick_turns_are_queued(monkeypatch):
    # Быстрое ↑, затем ← за один тик: второе нажатие не теряется.
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_UP),
        key_event(pygame.KSCAN_LEFT),
    )
    handle_keys(snake)
    assert snake.direction_queue == [UP, LEFT]
    snake.update_direction()
    assert snake.direction == UP
    snake.update_direction()
    assert snake.direction == LEFT


def test_reverse_of_queued_turn_is_blocked(monkeypatch):
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_UP),
        key_event(pygame.KSCAN_DOWN),
    )
    handle_keys(snake)
    assert snake.direction_queue == [UP]


def test_repeated_key_is_not_queued_twice(monkeypatch):
    snake = snake_moving(RIGHT)
    press(monkeypatch, key_event(pygame.KSCAN_UP), key_event(pygame.KSCAN_UP))
    handle_keys(snake)
    assert snake.direction_queue == [UP]


def test_queue_is_limited(monkeypatch):
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_UP),
        key_event(pygame.KSCAN_LEFT),
        key_event(pygame.KSCAN_DOWN),
    )
    handle_keys(snake)
    assert len(snake.direction_queue) == MAX_QUEUED_TURNS


def test_quit_event_exits(monkeypatch):
    # Не закрываем pygame по-настоящему: он нужен другим тестам.
    monkeypatch.setattr(pygame, 'quit', lambda: None)
    press(monkeypatch, pygame.event.Event(pygame.QUIT))
    with pytest.raises(SystemExit):
        handle_keys(Snake())


@pytest.mark.parametrize(
    'scancode', [pygame.KSCAN_P, pygame.KSCAN_ESCAPE], ids=['p', 'esc']
)
def test_pause_key_toggles_pause(monkeypatch, scancode):
    snake = Snake()
    press(monkeypatch, key_event(scancode))
    handle_keys(snake)
    assert snake.paused
    handle_keys(snake)
    assert not snake.paused


def test_direction_keys_are_ignored_on_pause(monkeypatch):
    snake = snake_moving(LEFT)
    snake.paused = True
    press(monkeypatch, key_event(pygame.KSCAN_UP))
    handle_keys(snake)
    assert snake.direction_queue == []
    assert snake.paused


def test_keys_ignored_right_after_game_over(monkeypatch):
    snake = Snake()
    snake.game_over = True
    snake.game_over_time = 5000
    monkeypatch.setattr(
        pygame.time, 'get_ticks', lambda: 5000 + GAME_OVER_DELAY - 1
    )
    press(monkeypatch, key_event(pygame.KSCAN_UP))
    handle_keys(snake)
    assert snake.game_over
    assert snake.direction_queue == []


def test_any_key_ends_game_over_after_delay(monkeypatch):
    snake = Snake()
    snake.game_over = True
    snake.game_over_time = 5000
    monkeypatch.setattr(
        pygame.time, 'get_ticks', lambda: 5000 + GAME_OVER_DELAY
    )
    press(monkeypatch, key_event(pygame.KSCAN_UP))
    handle_keys(snake)
    assert not snake.game_over


@pytest.mark.parametrize('scancode, direction', KEYS, ids=KEY_NAMES)
def test_pressed_key_is_held(monkeypatch, scancode, direction):
    snake = Snake()
    press(monkeypatch, key_event(scancode))
    handle_keys(snake)
    assert snake.held_direction == direction


def test_reverse_key_is_held_but_not_applied(monkeypatch):
    snake = snake_moving(RIGHT)
    press(monkeypatch, key_event(pygame.KSCAN_LEFT))
    handle_keys(snake)
    assert snake.held_direction == LEFT
    assert snake.direction_queue == []


def test_other_keys_keep_held_direction(monkeypatch):
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_RIGHT),
        key_event(pygame.KSCAN_SPACE),
    )
    handle_keys(snake)
    assert snake.held_direction == RIGHT


def test_releasing_held_key_clears_it(monkeypatch):
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_RIGHT),
        key_up_event(pygame.KSCAN_RIGHT),
    )
    handle_keys(snake)
    assert snake.held_direction is None


def test_releasing_other_key_keeps_held_direction(monkeypatch):
    snake = snake_moving(RIGHT)
    snake.held_direction = RIGHT
    press(monkeypatch, key_up_event(pygame.KSCAN_UP))
    handle_keys(snake)
    assert snake.held_direction == RIGHT


def test_last_pressed_key_replaces_held_direction(monkeypatch):
    # Помним только последнюю клавишу: после отпускания ↑ зажатая →
    # уже не учитывается.
    snake = snake_moving(RIGHT)
    press(
        monkeypatch,
        key_event(pygame.KSCAN_RIGHT),
        key_event(pygame.KSCAN_UP),
        key_up_event(pygame.KSCAN_UP),
    )
    handle_keys(snake)
    assert snake.held_direction is None


def test_direction_keys_are_not_held_on_pause(monkeypatch):
    snake = snake_moving(RIGHT)
    snake.paused = True
    press(monkeypatch, key_event(pygame.KSCAN_RIGHT))
    handle_keys(snake)
    assert snake.held_direction is None


def test_release_on_pause_clears_held_direction(monkeypatch):
    snake = snake_moving(RIGHT)
    snake.held_direction = RIGHT
    snake.paused = True
    press(monkeypatch, key_up_event(pygame.KSCAN_RIGHT))
    handle_keys(snake)
    assert snake.held_direction is None


def test_reset_clears_held_direction():
    snake = Snake()
    snake.held_direction = RIGHT
    snake.reset()
    assert snake.held_direction is None


def test_snake_is_boosted_when_holding_current_direction():
    snake = snake_moving(RIGHT)
    snake.held_direction = RIGHT
    assert snake.is_boosted()


@pytest.mark.parametrize(
    'held', [UP, DOWN, LEFT, None], ids=['up', 'down', 'reverse', 'none']
)
def test_snake_is_not_boosted_otherwise(held):
    snake = snake_moving(RIGHT)
    snake.held_direction = held
    assert not snake.is_boosted()


def boosted_snake(speed):
    """Создаёт змейку с заданной скоростью и зажатой клавишей хода."""
    snake = snake_moving(RIGHT)
    snake.held_direction = RIGHT
    snake.speed = speed
    return snake


@pytest.mark.parametrize(
    'speed, expected',
    [(3, 3 * BOOST_MULTIPLIER), (20, MAX_BOOST_SPEED), (31, 31)],
    ids=['multiplied', 'capped', 'not-slowed'],
)
def test_tick_speed_when_boosted(speed, expected):
    assert boosted_snake(speed).get_tick_speed() == expected


def test_tick_speed_without_boost():
    snake = snake_moving(RIGHT)
    snake.speed = 3
    assert snake.get_tick_speed() == 3
