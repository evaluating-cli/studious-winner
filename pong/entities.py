from dataclasses import dataclass, field

import pygame

if __package__ in (None, ""):
    from config import (
        BALL_SIZE,
        BALL_SPEED_X_PER_FRAME,
        HEIGHT,
        LEFT_PADDLE_X,
        PADDLE_HEIGHT,
        PADDLE_SPEED_PER_FRAME,
        PADDLE_WIDTH,
        WIDTH,
        WINNING_SCORE,
    )
else:
    from .config import (
        BALL_SIZE,
        BALL_SPEED_X_PER_FRAME,
        HEIGHT,
        LEFT_PADDLE_X,
        PADDLE_HEIGHT,
        PADDLE_SPEED_PER_FRAME,
        PADDLE_WIDTH,
        WIDTH,
        WINNING_SCORE,
    )


@dataclass
class Options:
    winning_score: int = WINNING_SCORE
    ball_speed_per_frame: int = BALL_SPEED_X_PER_FRAME
    paddle_speed_per_frame: int = PADDLE_SPEED_PER_FRAME


@dataclass
class Paddle:
    x: int
    y: int
    speed_per_frame: int = PADDLE_SPEED_PER_FRAME
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def reset(self):
        self.rect.x = self.x
        self.rect.y = self.y


@dataclass
class Ball:
    width: int = WIDTH
    height: int = HEIGHT
    speed_per_frame: int = BALL_SPEED_X_PER_FRAME
    vx_per_frame: int = field(init=False)
    vy_per_frame: int = field(init=False)
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            self.width // 2 - BALL_SIZE // 2,
            self.height // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.vx_per_frame = self.speed_per_frame
        self.vy_per_frame = self.speed_per_frame


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
        self.left_paddle = Paddle(LEFT_PADDLE_X, paddle_start_y, self.options.paddle_speed_per_frame)
        self.right_paddle = Paddle(self.width - PADDLE_WIDTH - LEFT_PADDLE_X, paddle_start_y, self.options.paddle_speed_per_frame)
        self.ball = Ball(self.width, self.height, self.options.ball_speed_per_frame)

    def reset(self):
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()
        self.score = [0, 0]
