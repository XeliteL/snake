"""Камни — препятствия на поле."""

from game_objects.cells import CellGroup
from settings import STONE_COLOR


class Stone(CellGroup):
    """Камни, которые появляются в случайных клетках поля."""

    def __init__(self, body_color=STONE_COLOR, positions=()):
        """Создаёт пустое поле камней."""
        super().__init__(body_color=body_color, positions=positions)
