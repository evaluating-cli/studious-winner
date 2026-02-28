import asyncio
import pygame

from config import (
    BALL_SIZE,
    BALL_SPEED_X_TUNED,
    BALL_SPEED_Y_TUNED,
    BLACK,
    CENTER_DASH_LENGTH,
    CENTER_LINE_WIDTH,
    CONTROLS_HINT_TEXT,
    FONT_NAME,
    FPS,
    HEIGHT,
    HINT_BOTTOM_MARGIN,
    HINT_COLOR,
    LEFT_WIN_TEXT,
    PADDLE_HEIGHT,
    PADDLE_LEFT_X,
    PADDLE_RIGHT_MARGIN,
    PADDLE_SPEED_TUNED,
    PADDLE_WIDTH,
    RESTART_TEXT,
    RESTART_TEXT_OFFSET_Y,
    RIGHT_WIN_TEXT,
    SCORE_FONT_SIZE,
    SCORE_TOP_MARGIN,
    SMALL_FONT_SIZE,
    WHITE,
    WIDTH,
    WINNER_TEXT_OFFSET_Y,
    WINNING_SCORE,
    WINDOW_CAPTION,
)


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED_TUNED

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PADDLE_HEIGHT))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.vx = BALL_SPEED_X_TUNED
        self.vy = BALL_SPEED_Y_TUNED

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


def draw_dashed_line(surface, color, start, end, dash_length=CENTER_DASH_LENGTH):
    x1, y1 = start
    x2, y2 = end
    dy = y2 - y1
    dashes = dy // (dash_length * 2)
    for i in range(dashes):
        start_y = y1 + i * dash_length * 2
        end_y = start_y + dash_length
        pygame.draw.line(surface, color, (x1, start_y), (x2, end_y), CENTER_LINE_WIDTH)


class GameState:
    def __init__(self):
        self.left_paddle = Paddle(PADDLE_LEFT_X, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(
            WIDTH - PADDLE_RIGHT_MARGIN,
            HEIGHT // 2 - PADDLE_HEIGHT // 2,
        )
        self.ball = Ball()
        self.score = [0, 0]

    def reset(self):
        self.left_paddle = Paddle(PADDLE_LEFT_X, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(
            WIDTH - PADDLE_RIGHT_MARGIN,
            HEIGHT // 2 - PADDLE_HEIGHT // 2,
        )
        self.ball.reset()
        self.score = [0, 0]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, SCORE_FONT_SIZE)
small_font = pygame.font.SysFont(FONT_NAME, SMALL_FONT_SIZE)


async def main():
    state = GameState()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state.left_paddle.move(pygame.K_w, pygame.K_s)
        state.right_paddle.move(pygame.K_UP, pygame.K_DOWN)

        state.ball.move()

        # Ball collision with paddles — push ball outside paddle to prevent tunnelling
        if state.ball.rect.colliderect(state.left_paddle.rect) and state.ball.vx < 0:
            state.ball.rect.left = state.left_paddle.rect.right
            state.ball.vx = -state.ball.vx
        if state.ball.rect.colliderect(state.right_paddle.rect) and state.ball.vx > 0:
            state.ball.rect.right = state.right_paddle.rect.left
            state.ball.vx = -state.ball.vx

        # Scoring
        if state.ball.rect.left <= 0:
            state.score[1] += 1
            state.ball.reset()
        elif state.ball.rect.right >= WIDTH:
            state.score[0] += 1
            state.ball.reset()

        # Draw center line
        draw_dashed_line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw paddles and ball
        state.left_paddle.draw(screen)
        state.right_paddle.draw(screen)
        state.ball.draw(screen)

        # Draw scores
        left_score = font.render(str(state.score[0]), True, WHITE)
        right_score = font.render(str(state.score[1]), True, WHITE)
        screen.blit(left_score, (WIDTH // 4 - left_score.get_width() // 2, SCORE_TOP_MARGIN))
        screen.blit(
            right_score,
            (3 * WIDTH // 4 - right_score.get_width() // 2, SCORE_TOP_MARGIN),
        )

        # Win condition
        winner = None
        if state.score[0] >= WINNING_SCORE:
            winner = LEFT_WIN_TEXT
        elif state.score[1] >= WINNING_SCORE:
            winner = RIGHT_WIN_TEXT

        if winner:
            msg = font.render(winner, True, WHITE)
            screen.blit(
                msg,
                (
                    WIDTH // 2 - msg.get_width() // 2,
                    HEIGHT // 2 + WINNER_TEXT_OFFSET_Y,
                ),
            )
            restart = small_font.render(RESTART_TEXT, True, WHITE)
            screen.blit(
                restart,
                (
                    WIDTH // 2 - restart.get_width() // 2,
                    HEIGHT // 2 + RESTART_TEXT_OFFSET_Y,
                ),
            )
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                state.reset()

        # Controls hint
        hint = small_font.render(CONTROLS_HINT_TEXT, True, HINT_COLOR)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - HINT_BOTTOM_MARGIN))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())
