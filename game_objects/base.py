"""Базовый класс игровых объектов."""

from random import randrange

import pygame

from display import screen
from settings import BORDER_COLOR, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    @staticmethod
    def random_cell(occupied=()):
        """Возвращает случайную клетку поля, которой нет в occupied."""
        while 1000 - 7:
            cell = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if cell not in occupied:
                return cell

    def draw_cell(self, position):
        """Рисует клетку цвета объекта с рамкой."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовывает объект на экране."""
        pass
