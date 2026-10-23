"""Набор клеток — общая основа для отравы и камней."""

from game_objects.base import GameObject


class CellGroup(GameObject):
    """Набор клеток одного цвета, которые добавляются по одной."""

    def __init__(self, body_color, positions=()):
        """Создаёт набор; по умолчанию он пустой."""
        super().__init__(body_color=body_color)
        self.positions = list(positions)

    def randomize_position(self, occupied=()):
        """Добавляет клетку в случайное свободное место и возвращает её."""
        new_position = self.random_cell(occupied)
        self.positions.append(new_position)
        return new_position

    def draw(self):
        """Отрисовывает последнюю добавленную клетку."""
        self.draw_cell(self.positions[-1])

    def reset(self):
        """Убирает все клетки с поля."""
        self.positions = []
