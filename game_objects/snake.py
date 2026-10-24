"""Змейка, управляемая игроком."""

import pygame

from game_objects.base import GameObject
from settings import (
    GRID_SIZE, RIGHT, SCREEN_HEIGHT,
    SCREEN_WIDTH, SNAKE_COLOR, START_SPEED
)


class Snake(GameObject):
    """Змейка, управляемая игроком.

    Хранит позиции сегментов тела, длину, направление движения, скорость,
    а также состояние паузы, проигрыша и победы.
    """

    def __init__(
            self,
            length=1,
            positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
            direction=RIGHT,
            next_direction=None,
            body_color=SNAKE_COLOR,
            speed=START_SPEED,
            paused=False,
            game_over=False,
            game_over_time=0,
            won=False,
    ):
        """Создаёт змейку в центре поля."""
        super().__init__(body_color=body_color)
        self.length = length
        self.positions = list(positions)
        self.direction = direction
        self.next_direction = next_direction
        self.speed = speed
        self.paused = paused
        self.game_over = game_over
        self.game_over_time = game_over_time
        self.won = won

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
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            self.draw_cell(position)

    def delete_tail(self):
        """Укорачивает змейку на один сегмент."""
        self.length -= 1
        self.positions.pop()

    def die(self):
        """Завершает партию и запоминает время проигрыша."""
        self.game_over = True
        self.game_over_time = pygame.time.get_ticks()

    def win(self):
        """Завершает партию победой."""
        self.won = True
        self.die()

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.speed = START_SPEED
        self.paused = False
        self.game_over = False
        self.game_over_time = 0
        self.won = False
