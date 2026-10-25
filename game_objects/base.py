"""Базовый класс игровых объектов."""

from random import choice

import pygame

from display import screen
from settings import BORDER_COLOR, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

ALL_CELLS = [
    (x, y)
    for x in range(0, SCREEN_WIDTH, GRID_SIZE)
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
]


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
            self,
            position=(0, 0),
            body_color=(255, 255, 255),
            border_radius=0
    ):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color
        self.border_radius = border_radius

    @staticmethod
    def random_cell(occupied=()):
        """Возвращает случайную клетку поля, которой нет в occupied.

        Выбирает из списка свободных клеток, поэтому не зависает на
        заполненном поле; если свободных клеток нет, возвращает None.
        """
        occupied = set(occupied)
        free_cells = [cell for cell in ALL_CELLS if cell not in occupied]
        if free_cells:
            return choice(free_cells)
        return None

    def draw_cell(self, position, corners=None):
        """Рисует клетку цвета объекта с рамкой."""
        if corners is None:
            corners = {}

        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(
            screen,
            self.body_color,
            rect,
            border_radius=self.border_radius,
            **corners
        )
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            rect,
            1,
            border_radius=self.border_radius,
            **corners
        )

    def draw(self):
        """Отрисовывает объект на экране."""
        pass
