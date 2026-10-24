"""Окно игры, таймер и надписи паузы, проигрыша и победы."""
import pygame

from settings import (
    BOARD_BACKGROUND_COLOR, FONT_SIZE, GAME_OVER_COLOR, HINT_COLOR,
    HINT_FONT_SIZE, OVERLAY_ALPHA, SCREEN_HEIGHT, SCREEN_WIDTH,
    SHADOW_COLOR, SHADOW_OFFSET, TEXT_COLOR, VICTORY_COLOR
)

screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
window = None
clock = pygame.time.Clock()


def init_display():
    """Открывает окно игры."""
    global window
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Змейка")


def copy_screen():
    """Копирует нарисованный кадр в окно и показывает его."""
    window.blit(screen, (0, 0))
    pygame.display.update()


def draw_overlay():
    """Затемняет всё поле полупрозрачным слоем."""
    overlay = pygame.Surface(screen.get_size())
    overlay.fill(BOARD_BACKGROUND_COLOR)
    overlay.set_alpha(OVERLAY_ALPHA)
    screen.blit(overlay, (0, 0))


def draw_text(message, size, color, center):
    """Рисует текст с тенью, центрируя его в точке center."""
    font = pygame.font.Font(None, size)
    shadow = font.render(message, True, SHADOW_COLOR)
    text = font.render(message, True, color)
    shadow_center = (center[0] + SHADOW_OFFSET, center[1] + SHADOW_OFFSET)
    screen.blit(shadow, shadow.get_rect(center=shadow_center))
    screen.blit(text, text.get_rect(center=center))


def draw_message(title, hint, color=TEXT_COLOR):
    """Затемняет поле и рисует крупный заголовок с подсказкой под ним."""
    draw_overlay()
    center_x, center_y = screen.get_rect().center
    draw_text(title, FONT_SIZE, color, (center_x, center_y - FONT_SIZE // 4))
    draw_text(hint, HINT_FONT_SIZE, HINT_COLOR,
              (center_x, center_y + FONT_SIZE // 2))


def draw_pause():
    """Рисует надпись «Пауза» по центру экрана."""
    draw_message('Пауза', 'P или Esc — продолжить')


def draw_game_over():
    """Рисует надпись «Игра окончена» по центру экрана."""
    draw_message('Игра окончена', 'Нажмите любую клавишу', GAME_OVER_COLOR)


def draw_victory():
    """Рисует надпись «Победа!» по центру экрана."""
    draw_message('Победа!', 'Нажмите любую клавишу', VICTORY_COLOR)
