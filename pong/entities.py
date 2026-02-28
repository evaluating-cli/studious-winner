from dataclasses import dataclass, field

import pygame

if __package__ in (None, ""):
    from config import (
        BALL_SIZE,
        BALL_SPEED_X,
        BALL_SPEED_Y,
        HEIGHT,
        LEFT_PADDLE_X,
        PADDLE_HEIGHT,
        PADDLE_SPEED,
        PADDLE_WIDTH,
        WIDTH,
    )
else:
    from .config import (
        BALL_SIZE,
        BALL_SPEED_X,
        BALL_SPEED_Y,
        HEIGHT,
        LEFT_PADDLE_X,
        PADDLE_HEIGHT,
        PADDLE_SPEED,
        PADDLE_WIDTH,
        WIDTH,
    )


@dataclass
class Paddle:
    x: int
    y: int
    speed: int = PADDLE_SPEED
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
    vx: int = BALL_SPEED_X
    vy: int = BALL_SPEED_Y
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
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y


@dataclass
class GameState:
    width: int = WIDTH
    height: int = HEIGHT
    left_paddle: Paddle = field(init=False)
    right_paddle: Paddle = field(init=False)
    ball: Ball = field(init=False)
    score: list[int] = field(default_factory=lambda: [0, 0])

    def __post_init__(self):
        paddle_start_y = self.height // 2 - PADDLE_HEIGHT // 2
        self.left_paddle = Paddle(LEFT_PADDLE_X, paddle_start_y)
        self.right_paddle = Paddle(self.width - PADDLE_WIDTH - LEFT_PADDLE_X, paddle_start_y)
        self.ball = Ball(self.width, self.height)

    def reset(self):
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()
        self.score = [0, 0]
