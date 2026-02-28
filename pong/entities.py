from dataclasses import dataclass, field

import pygame

from .config import (
    BALL_SIZE,
    BALL_SPEED_X,
    HEIGHT,
    LEFT_PADDLE_X,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    WIDTH,
    WINNING_SCORE,
)


@dataclass
class Options:
    winning_score: int = WINNING_SCORE
    ball_speed: int = BALL_SPEED_X
    paddle_speed: int = PADDLE_SPEED


@dataclass
class Paddle:
    x: int
    y: int
    speed: float = PADDLE_SPEED  # pixels per second
    y_pos: float = field(init=False)
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.y_pos = float(self.y)
        self.rect = pygame.Rect(self.x, int(self.y_pos), PADDLE_WIDTH, PADDLE_HEIGHT)

    def sync_rect(self):
        self.rect.x = self.x
        self.rect.y = int(round(self.y_pos))

    def reset(self):
        self.y_pos = float(self.y)
        self.sync_rect()


@dataclass
class Ball:
    width: int = WIDTH
    height: int = HEIGHT
    speed: float = BALL_SPEED_X  # pixels per second on each axis
    x_pos: float = field(init=False)
    y_pos: float = field(init=False)
    vx: float = field(init=False)
    vy: float = field(init=False)
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.reset()

    def sync_rect(self):
        self.rect.x = int(round(self.x_pos))
        self.rect.y = int(round(self.y_pos))

    def reset(self):
        self.x_pos = float(self.width // 2 - BALL_SIZE // 2)
        self.y_pos = float(self.height // 2 - BALL_SIZE // 2)
        self.rect = pygame.Rect(int(self.x_pos), int(self.y_pos), BALL_SIZE, BALL_SIZE)
        self.vx = float(self.speed)
        self.vy = float(self.speed)


@dataclass
class GameState:
    width: int = WIDTH
    height: int = HEIGHT
    options: Options = field(default_factory=Options)
    left_paddle: Paddle = field(init=False)
    right_paddle: Paddle = field(init=False)
    ball: Ball = field(init=False)
    score: list[int] = field(default_factory=lambda: [0, 0])
    winning_score: int = field(init=False)

    def __post_init__(self):
        self.winning_score = self.options.winning_score
        paddle_start_y = self.height // 2 - PADDLE_HEIGHT // 2
        self.left_paddle = Paddle(LEFT_PADDLE_X, paddle_start_y, self.options.paddle_speed)
        self.right_paddle = Paddle(self.width - PADDLE_WIDTH - LEFT_PADDLE_X, paddle_start_y, self.options.paddle_speed)
        self.ball = Ball(self.width, self.height, self.options.ball_speed)

    def reset(self):
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()
        self.score = [0, 0]
