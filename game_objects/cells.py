"""Набор клеток — общая основа для отравы и камней."""

from game_objects.base import GameObject


class CellGroup(GameObject):
    """Набор клеток одного цвета, которые добавляются по одной."""

    def __init__(self, body_color, positions=(), border_radius=0):
        """Создаёт набор; по умолчанию он пустой."""
        super().__init__(body_color=body_color, border_radius=border_radius)
        self.positions = list(positions)

    def randomize_position(self, occupied=()):
        """Добавляет клетку в случайное свободное место и возвращает её.

        Если свободных клеток нет, ничего не добавляет и возвращает None.
        """
        new_position = self.random_cell(occupied)
        if new_position is not None:
            self.positions.append(new_position)
        return new_position

    def draw(self):
        """Отрисовывает все клетки набора."""
        for position in self.positions:
            self.draw_cell(position)

    def reset(self):
        """Убирает все клетки с поля."""
        self.positions = []
