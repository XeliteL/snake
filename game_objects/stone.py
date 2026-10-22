"""Камни — препятствия на поле."""

from random import randrange

import pygame

from display import screen
from game_objects.base import GameObject
from settings import (
    BORDER_COLOR, GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, STONE_COLOR
)


class Stone(GameObject):
    """Камни, которые появляются в случайных клетках поля."""

    def __init__(
            self,
            body_color=STONE_COLOR,
            positions=()
    ):
        """Создаёт пустое поле камней."""
        super().__init__(body_color=body_color)
        self.positions = list(positions)

    def randomize_position(self, occupied=()):
        """Добавляет камень в случайную свободную клетку.

        Возвращает список всех камней.
        """
        while 1000 - 7:
            new_position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if new_position not in occupied:
                self.positions.append(new_position)
                return self.positions

    def draw(self):
        """Отрисовывает последний добавленный камень."""
        rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Убирает все камни с поля."""
        self.positions = []
