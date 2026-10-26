"""Еда: яблоко, волшебное яблоко и отрава."""

from game_objects.base import GameObject
from game_objects.cells import CellGroup
from settings import (
    APPLE_COLOR, BORDER_RADIUS, MAGIC_APPLE_COLOR, POISON_COLOR,
)


class Food(GameObject):
    """Еда, которая появляется в случайной клетке поля."""

    def __init__(self, body_color, border_radius=0):
        """Задаёт цвет еды; позицию выбирают наследники."""
        super().__init__(body_color=body_color, border_radius=border_radius)

    def randomize_position(self, occupied=()):
        """Перемещает еду в случайную клетку и возвращает её.

        Если свободных клеток нет, еда остаётся на месте.
        """
        new_position = self.random_cell(occupied)
        if new_position is not None:
            self.position = new_position
        return self.position

    def draw(self):
        """Отрисовывает еду на экране."""
        self.draw_cell(self.position)


class Apple(Food):
    """Яблоко, которое появляется в случайной клетке поля."""

    def __init__(
            self,
            body_color=APPLE_COLOR,
            occupied=(),
            border_radius=BORDER_RADIUS
    ):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(body_color=body_color, border_radius=border_radius)
        self.randomize_position(occupied)


class MagicApple(CellGroup):
    """Волшебное яблоко: даёт много очков.

    Появляется не с начала игры, а иногда на максимальной скорости;
    на поле бывает не больше одного.
    """

    def __init__(
            self,
            body_color=MAGIC_APPLE_COLOR,
            positions=(),
            border_radius=BORDER_RADIUS
    ):
        """Создаёт волшебное яблоко; по умолчанию на поле его нет."""
        super().__init__(
            body_color=body_color,
            positions=positions,
            border_radius=border_radius
        )


class Poison(CellGroup):
    """Отрава: клетки, которые укорачивают змейку.

    Появляется не с начала игры, а каждые 10 яблок.
    """

    def __init__(
            self,
            body_color=POISON_COLOR,
            positions=(),
            border_radius=BORDER_RADIUS
    ):
        """Создаёт отраву; по умолчанию на поле её нет."""
        super().__init__(
            body_color=body_color,
            positions=positions,
            border_radius=border_radius
        )
