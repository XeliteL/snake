"""Окно игры и таймер."""

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()
