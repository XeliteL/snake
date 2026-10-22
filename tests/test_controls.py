"""Тесты управления змейкой из controls.py."""

import pygame
import pytest

from controls import handle_keys
from game_objects import Snake
from settings import DOWN, LEFT, RIGHT, UP

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
    assert snake.next_direction == direction


@pytest.mark.parametrize('scancode, direction', KEYS, ids=KEY_NAMES)
def test_reverse_is_blocked(monkeypatch, scancode, direction):
    snake = snake_moving(OPPOSITE[direction])
    press(monkeypatch, key_event(scancode))
    handle_keys(snake)
    assert snake.next_direction is None


def test_wasd_works_with_russian_layout(monkeypatch):
    snake = snake_moving(LEFT)
    # Физическая W при русской раскладке даёт символ «ц».
    press(monkeypatch, key_event(pygame.KSCAN_W, key=ord('ц')))
    handle_keys(snake)
    assert snake.next_direction == UP


def test_other_keys_are_ignored(monkeypatch):
    snake = snake_moving(RIGHT)
    press(monkeypatch, key_event(pygame.KSCAN_SPACE))
    handle_keys(snake)
    assert snake.next_direction is None
    assert snake.direction == RIGHT


def test_quit_event_exits(monkeypatch):
    # Не закрываем pygame по-настоящему: он нужен другим тестам.
    monkeypatch.setattr(pygame, 'quit', lambda: None)
    press(monkeypatch, pygame.event.Event(pygame.QUIT))
    with pytest.raises(SystemExit):
        handle_keys(Snake())
