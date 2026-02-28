"""Configuration for Pong gameplay, visuals, and tunable web overrides."""

from __future__ import annotations

import os


def _env_int(name: str, default: int, minimum: int = 1) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return max(minimum, int(value))
    except ValueError:
        return default


def _env_float(name: str, default: float, minimum: float = 0.1) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return max(minimum, float(value))
    except ValueError:
        return default


# Dimensions
WIDTH = 640
HEIGHT = 480
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
PADDLE_LEFT_X = 20
PADDLE_RIGHT_MARGIN = 30
BALL_SIZE = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HINT_COLOR = (150, 150, 150)

# Timing and movement
FPS = 60
PADDLE_SPEED = 6
BALL_BASE_SPEED_X = 5
BALL_BASE_SPEED_Y = 5

# Web/host tuning overrides
SPEED_MULTIPLIER = _env_float("SPEED_MULTIPLIER", 1.0)
PADDLE_SPEED_MULTIPLIER = _env_float("PADDLE_SPEED_MULTIPLIER", SPEED_MULTIPLIER)
BALL_SPEED_MULTIPLIER = _env_float("BALL_SPEED_MULTIPLIER", SPEED_MULTIPLIER)

PADDLE_SPEED_TUNED = max(1, int(PADDLE_SPEED * PADDLE_SPEED_MULTIPLIER))
BALL_SPEED_X_TUNED = max(1, int(BALL_BASE_SPEED_X * BALL_SPEED_MULTIPLIER))
BALL_SPEED_Y_TUNED = max(1, int(BALL_BASE_SPEED_Y * BALL_SPEED_MULTIPLIER))

# Score and win conditions
WINNING_SCORE = _env_int("WINNING_SCORE", 7)

# Typography and UI text
FONT_NAME = "monospace"
SCORE_FONT_SIZE = 48
SMALL_FONT_SIZE = 20
WINDOW_CAPTION = "Pong"
RESTART_TEXT = "Press R to restart"
CONTROLS_HINT_TEXT = "W/S  vs  UP/DOWN"
LEFT_WIN_TEXT = "Left Player Wins!"
RIGHT_WIN_TEXT = "Right Player Wins!"

# UI positioning
SCORE_TOP_MARGIN = 20
WINNER_TEXT_OFFSET_Y = -40
RESTART_TEXT_OFFSET_Y = 20
HINT_BOTTOM_MARGIN = 25

# Dash line settings
CENTER_LINE_WIDTH = 2
CENTER_DASH_LENGTH = 10
