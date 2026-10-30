"""Змейка, управляемая игроком."""

import pygame

from game_objects.base import GameObject
from settings import (
    BOOST_MULTIPLIER, GRID_SIZE, MAX_BOOST_SPEED, MAX_QUEUED_TURNS,
    RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, SNAKE_COLOR, SNAKE_CORNERS,
    START_SCORE, START_SPEED,
)


class Snake(GameObject):
    """Змейка, управляемая игроком.

    Хранит позиции сегментов тела, длину, направление движения,
    зажатое игроком направление, скорость, а также состояние паузы,
    проигрыша и победы.
    """

    def __init__(
            self,
            length=1,
            positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
            direction=RIGHT,
            direction_queue=(),
            held_direction=None,
            body_color=SNAKE_COLOR,
            speed=START_SPEED,
            score=START_SCORE,
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
        self.direction_queue = list(direction_queue)
        self.held_direction = held_direction
        self.speed = speed
        self.score = score
        self.paused = paused
        self.game_over = game_over
        self.game_over_time = game_over_time
        self.won = won

    def queue_direction(self, direction):
        """Добавляет поворот в очередь нажатий.

        Поворот сравнивается с последним направлением в очереди, а если
        она пуста, то с текущим. Повтор того же направления и разворот
        на 180 градусов игнорируются, как и нажатия сверх
        MAX_QUEUED_TURNS.
        """
        last = self.direction_queue[-1] if self.direction_queue else (
            self.direction
        )
        if (direction == last
                or direction == (-last[0], -last[1])
                or len(self.direction_queue) >= MAX_QUEUED_TURNS):
            return
        self.direction_queue.append(direction)

    def update_direction(self):
        """Применяет первый поворот из очереди нажатий."""
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)

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

    def is_boosted(self):
        """Проверяет, зажата ли клавиша текущего направления."""
        return self.held_direction == self.direction

    def get_tick_speed(self):
        """Возвращает скорость для clock.tick с учётом ускорения.

        Пока зажата клавиша текущего направления, скорость умножается
        на BOOST_MULTIPLIER, но не выше MAX_BOOST_SPEED. Если змейка
        уже быстрее MAX_BOOST_SPEED, ускорение её не замедляет.
        """
        if self.is_boosted() and self.speed < MAX_BOOST_SPEED:
            return min(self.speed * BOOST_MULTIPLIER, MAX_BOOST_SPEED)
        return self.speed

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def get_tail_position(self):
        """Возвращает позицию хвоста змейки."""
        return self.positions[-1]

    @staticmethod
    def get_step(delta, size):
        """Переводит разницу координат соседних клеток в -1, 0 или 1.

        Остаток от деления на size убирает переход через край поля:
        остаются только 0, GRID_SIZE (шаг вперёд) и size - GRID_SIZE
        (шаг назад).
        """
        delta %= size
        if delta == 0:
            return 0
        if delta == GRID_SIZE:
            return 1
        return -1

    def get_tail_direction(self):
        """Возвращает направление хвоста змейки — от тела наружу."""
        tail_x, tail_y = self.get_tail_position()
        before_tail_x, before_tail_y = self.positions[-2]
        return (
            self.get_step(tail_x - before_tail_x, SCREEN_WIDTH),
            self.get_step(tail_y - before_tail_y, SCREEN_HEIGHT)
        )

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        if len(self.positions) > 1:
            for position in self.positions[1:-1]:
                self.draw_cell(position)
            self.draw_cell(
                self.positions[0], SNAKE_CORNERS[self.direction]
            )
            self.draw_cell(
                self.positions[-1],
                SNAKE_CORNERS[self.get_tail_direction()]
            )
        else:
            self.draw_cell(self.positions[0], SNAKE_CORNERS["ALL"])

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
        self.direction_queue = []
        self.held_direction = None
        self.speed = START_SPEED
        self.score = START_SCORE
        self.paused = False
        self.game_over = False
        self.game_over_time = 0
        self.won = False
