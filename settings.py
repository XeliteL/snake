"""Настройки игры: размеры поля, цвета, направления и скорость."""

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
POISON_COLOR = (0, 0, 255)
STONE_COLOR = (120, 120, 120)
TEXT_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 80, 80)
VICTORY_COLOR = (0, 204, 51)
HINT_COLOR = (180, 180, 180)
SHADOW_COLOR = (0, 0, 0)
SHADOW_OFFSET = 4
OVERLAY_ALPHA = 160
BORDER_RADIUS = 8
SNAKE_CORNERS = {
    UP: {
        "border_top_left_radius": BORDER_RADIUS,
        "border_top_right_radius": BORDER_RADIUS,
    },
    RIGHT: {
        "border_top_right_radius": BORDER_RADIUS,
        "border_bottom_right_radius": BORDER_RADIUS,
    },
    DOWN: {
        "border_bottom_left_radius": BORDER_RADIUS,
        "border_bottom_right_radius": BORDER_RADIUS,
    },
    LEFT: {
        "border_top_left_radius": BORDER_RADIUS,
        "border_bottom_left_radius": BORDER_RADIUS,
    },
    "ALL": {
        "border_top_left_radius": BORDER_RADIUS,
        "border_top_right_radius": BORDER_RADIUS,
        "border_bottom_left_radius": BORDER_RADIUS,
        "border_bottom_right_radius": BORDER_RADIUS,
    },
}
FONT_SIZE = 72
HINT_FONT_SIZE = 28
GAME_OVER_DELAY = 1000
START_SPEED = 3

MAX_SPEED = 25
FAST_SPEED = 15
SLOW_SPEED_STEP = 0.5
FAST_SPEED_STEP = 0.2
MAX_SPEED_STEP = 0.1
POISON_EVERY_APPLES = 10
MAX_STONES = 10
WIN_LENGTH = 100
