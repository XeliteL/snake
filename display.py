"""Окно игры, таймер и надпись паузы."""

import pygame

from settings import (
    FONT_SIZE, TEXT_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH
)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


def draw_message(message):
    """Рисует надпись по центру экрана."""
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(text, text.get_rect(center=screen.get_rect().center))


def draw_pause():
    """Рисует надпись «Пауза» по центру экрана."""
    draw_message('Пауза')
