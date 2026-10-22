"""Еда: яблоко и отрава."""

from random import randrange

import pygame

from display import screen
from game_objects.base import GameObject
from settings import (
    APPLE_COLOR, BORDER_COLOR, GRID_SIZE, POISON_COLOR, SCREEN_HEIGHT,
    SCREEN_WIDTH
)


class Food(GameObject):
    """Еда, которая появляется в случайной клетке поля."""

    def __init__(self, body_color):
        """Задаёт цвет еды; позицию выбирают наследники."""
        super().__init__(body_color=body_color)

    def randomize_position(self, occupied=()):
        """Перемещает еду в случайную клетку и возвращает её."""
        while 1000 - 7:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if self.position not in occupied:
                return self.position

    def draw(self):
        """Отрисовывает еду на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(Food):
    """Яблоко, которое появляется в случайной клетке поля."""

    def __init__(self, body_color=APPLE_COLOR, occupied=()):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied)


class Poison(Food):
    """Отрава: клетки, которые укорачивают змейку.

    Появляется не с начала игры, а каждые 10 яблок.
    """

    def __init__(self, body_color=POISON_COLOR, positions=()):
        """Создаёт отраву; по умолчанию на поле её нет."""
        super().__init__(body_color=body_color)
        self.positions = list(positions)

    def randomize_position(self, occupied=()):
        """Добавляет отраву в случайную свободную клетку и возвращает её."""
        while 1000 - 7:
            new_position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if new_position not in occupied:
                self.positions.append(new_position)
                return new_position

    def draw(self):
        """Отрисовывает последнюю добавленную отраву."""
        rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Убирает всю отраву с поля."""
        self.positions = []
