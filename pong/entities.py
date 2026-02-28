from dataclasses import dataclass, field

import pygame

from pong.config import (
    BALL_SIZE,
    BALL_SPEED_X,
    BALL_SPEED_Y,
    HEIGHT,
    LEFT_PADDLE_X,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_START_Y,
    PADDLE_WIDTH,
    RIGHT_PADDLE_X,
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
    vx: int = BALL_SPEED_X
    vy: int = BALL_SPEED_Y
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y


@dataclass
class GameState:
    left_paddle: Paddle = field(default_factory=lambda: Paddle(LEFT_PADDLE_X, PADDLE_START_Y))
    right_paddle: Paddle = field(default_factory=lambda: Paddle(RIGHT_PADDLE_X, PADDLE_START_Y))
    ball: Ball = field(default_factory=Ball)
    score: list[int] = field(default_factory=lambda: [0, 0])

    def reset(self):
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()
        self.score = [0, 0]
