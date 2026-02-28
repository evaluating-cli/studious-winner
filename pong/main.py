import asyncio
import pygame

# Constants
WIDTH, HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 15
FPS = 60
WINNING_SCORE = 7


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 6

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
        self.vx = 5
        self.vy = 5

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


def draw_dashed_line(surface, color, start, end, dash_length=10):
    x1, y1 = start
    x2, y2 = end
    dy = y2 - y1
    dashes = dy // (dash_length * 2)
    for i in range(dashes):
        start_y = y1 + i * dash_length * 2
        end_y = start_y + dash_length
        pygame.draw.line(surface, color, (x1, start_y), (x2, end_y), 2)


class GameState:
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self):
        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.score = [0, 0]
        self.phase = self.PLAYING

    @property
    def winner(self):
        if self.score[0] >= WINNING_SCORE:
            return "Left Player Wins!"
        if self.score[1] >= WINNING_SCORE:
            return "Right Player Wins!"
        return None

    def reset(self):
        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball.reset()
        self.score = [0, 0]
        self.phase = self.PLAYING


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 48)
small_font = pygame.font.SysFont("monospace", 20)


async def main():
    state = GameState()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if state.phase == GameState.PLAYING:
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

            if state.winner:
                state.phase = GameState.GAME_OVER
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                state.reset()

        # Draw center line
        draw_dashed_line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw paddles and ball
        state.left_paddle.draw(screen)
        state.right_paddle.draw(screen)
        state.ball.draw(screen)

        # Draw scores
        left_score = font.render(str(state.score[0]), True, WHITE)
        right_score = font.render(str(state.score[1]), True, WHITE)
        screen.blit(left_score, (WIDTH // 4 - left_score.get_width() // 2, 20))
        screen.blit(right_score, (3 * WIDTH // 4 - right_score.get_width() // 2, 20))

        # Win screen
        if state.phase == GameState.GAME_OVER and state.winner:
            msg = font.render(state.winner, True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            restart = small_font.render("Press R to restart", True, WHITE)
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

        # Controls hint
        hint = small_font.render("W/S  vs  UP/DOWN", True, (150, 150, 150))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 25))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())
