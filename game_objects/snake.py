"""Змейка, управляемая игроком."""

import pygame

from display import screen
from game_objects.base import GameObject
from settings import (
    BOARD_BACKGROUND_COLOR, BORDER_COLOR, GRID_SIZE, RIGHT, SCREEN_HEIGHT,
    SCREEN_WIDTH, SNAKE_COLOR, START_SPEED
)


class Snake(GameObject):
    """Змейка, управляемая игроком.

    Хранит позиции сегментов тела, длину и направление движения.
    """

    def __init__(
            self,
            length=1,
            positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
            direction=RIGHT,
            next_direction=None,
            last=None,
            body_color=SNAKE_COLOR,
            speed=START_SPEED
    ):
        """Создаёт змейку в центре поля."""
        super().__init__(body_color=body_color)
        self.length = length
        self.positions = list(positions)
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        self.speed = speed

    def update_direction(self):
        """Применяет направление, выбранное игроком."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвигает змейку на одну клетку с переходом через края поля."""
        new_head = (
            (self.positions[0][0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку и затирает след хвоста."""
        for position in self.positions[1:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def delete_tail(self):
        """Укорачивает змейку на один сегмент и стирает его с экрана."""
        self.length -= 1
        tail = self.positions.pop()
        tail_rect = pygame.Rect(tail, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, tail_rect)

    def reset(self):
        """Возвращает змейку в начальное состояние и очищает экран."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.speed = START_SPEED
        screen.fill(BOARD_BACKGROUND_COLOR)
