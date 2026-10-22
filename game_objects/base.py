"""Базовый класс игровых объектов."""


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Задаёт позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране."""
        pass
