"""Еда: яблоко и отрава."""

from game_objects.base import GameObject
from game_objects.cells import CellGroup
from settings import APPLE_COLOR, POISON_COLOR


class Food(GameObject):
    """Еда, которая появляется в случайной клетке поля."""

    def __init__(self, body_color):
        """Задаёт цвет еды; позицию выбирают наследники."""
        super().__init__(body_color=body_color)

    def randomize_position(self, occupied=()):
        """Перемещает еду в случайную клетку и возвращает её."""
        self.position = self.random_cell(occupied)
        return self.position

    def draw(self):
        """Отрисовывает еду на экране."""
        self.draw_cell(self.position)


class Apple(Food):
    """Яблоко, которое появляется в случайной клетке поля."""

    def __init__(self, body_color=APPLE_COLOR, occupied=()):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(body_color=body_color)
        self.randomize_position(occupied)


class Poison(CellGroup):
    """Отрава: клетки, которые укорачивают змейку.

    Появляется не с начала игры, а каждые 10 яблок.
    """

    def __init__(self, body_color=POISON_COLOR, positions=()):
        """Создаёт отраву; по умолчанию на поле её нет."""
        super().__init__(body_color=body_color, positions=positions)
