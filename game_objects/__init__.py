"""Игровые объекты: базовый класс, еда (яблоко и отрава), змейка и камни."""

from game_objects.base import GameObject
from game_objects.cells import CellGroup
from game_objects.food import Apple, Food, Poison
from game_objects.snake import Snake
from game_objects.stone import Stone

__all__ = [
    'Apple', 'CellGroup', 'Food', 'GameObject', 'Poison', 'Snake', 'Stone'
]
