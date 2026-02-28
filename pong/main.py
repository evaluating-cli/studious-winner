import asyncio
from dataclasses import dataclass, field

import pygame

if __package__ in (None, ""):
    from config import (
        BALL_SIZE,
        BALL_SPEED_X,
        BALL_SPEED_Y,
        BLACK,
        FPS,
        HEIGHT,
        PADDLE_HEIGHT,
        PADDLE_SPEED,
        PADDLE_WIDTH,
        WHITE,
        WINNING_SCORE,
    )
else:
    from .config import (
        BALL_SIZE,
        BALL_SPEED_X,
        BALL_SPEED_Y,
        BLACK,
        FPS,
        HEIGHT,
        PADDLE_HEIGHT,
        PADDLE_SPEED,
        PADDLE_WIDTH,
        WHITE,
        WINNING_SCORE,
    )

NORMAL_WIDTH = 640
WIDESCREEN_WIDTH = 960

PHASE_MENU = "menu"
PHASE_OPTIONS = "options"
PHASE_PLAYING = "playing"


@dataclass
class Options:
    widescreen: bool = False

    @property
    def width(self) -> int:
        return WIDESCREEN_WIDTH if self.widescreen else NORMAL_WIDTH


@dataclass
class Paddle:
    x: int
    y: int
    speed: int = PADDLE_SPEED
    rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction: int, height: int):
        self.rect.y += direction * self.speed
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def reset(self):
        self.rect.x = self.x
        self.rect.y = self.y


@dataclass
class Ball:
    width: int
    height: int
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
    width: int
    height: int
    left_paddle: Paddle = field(init=False)
    right_paddle: Paddle = field(init=False)
    ball: Ball = field(init=False)
    score: list[int] = field(default_factory=lambda: [0, 0])

    def __post_init__(self):
        paddle_start_y = self.height // 2 - PADDLE_HEIGHT // 2
        self.left_paddle = Paddle(20, paddle_start_y)
        self.right_paddle = Paddle(self.width - 30, paddle_start_y)
        self.ball = Ball(self.width, self.height)

    def reset(self):
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.width = self.width
        self.ball.height = self.height
        self.ball.reset()
        self.score = [0, 0]


def draw_dashed_line(surface, color, start, end, dash_length=10):
    x1, y1 = start
    x2, y2 = end
    dy = y2 - y1
    dashes = dy // (dash_length * 2)
    for i in range(dashes):
        start_y = y1 + i * dash_length * 2
        end_y = start_y + dash_length
        pygame.draw.line(surface, color, (x1, start_y), (x2, end_y), 2)


def draw_menu(screen, width, height, font, small_font):
    screen.fill(BLACK)
    title = font.render("PONG", True, WHITE)
    start = small_font.render("Press ENTER to start", True, WHITE)
    opts = small_font.render("Press O for options", True, WHITE)

    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 80))
    screen.blit(start, (width // 2 - start.get_width() // 2, height // 2))
    screen.blit(opts, (width // 2 - opts.get_width() // 2, height // 2 + 35))
    pygame.display.flip()


def draw_options(screen, options, width, height, font, small_font):
    screen.fill(BLACK)
    title = font.render("OPTIONS", True, WHITE)
    ws_value = "ON" if options.widescreen else "OFF"
    ws_label = small_font.render(f"Widescreen: {ws_value} (ENTER to toggle)", True, WHITE)
    back = small_font.render("ESC to go back", True, WHITE)

    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 80))
    screen.blit(ws_label, (width // 2 - ws_label.get_width() // 2, height // 2))
    screen.blit(back, (width // 2 - back.get_width() // 2, height // 2 + 35))
    pygame.display.flip()


def draw_playing(screen, state, font, small_font):
    screen.fill(BLACK)

    draw_dashed_line(screen, WHITE, (state.width // 2, 0), (state.width // 2, state.height))

    pygame.draw.rect(screen, WHITE, state.left_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.right_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.ball.rect)

    left_score = font.render(str(state.score[0]), True, WHITE)
    right_score = font.render(str(state.score[1]), True, WHITE)
    screen.blit(left_score, (state.width // 4 - left_score.get_width() // 2, 20))
    screen.blit(right_score, (3 * state.width // 4 - right_score.get_width() // 2, 20))

    winner = None
    if state.score[0] >= WINNING_SCORE:
        winner = "Left Player Wins!"
    elif state.score[1] >= WINNING_SCORE:
        winner = "Right Player Wins!"

    if winner:
        msg = font.render(winner, True, WHITE)
        screen.blit(msg, (state.width // 2 - msg.get_width() // 2, state.height // 2 - 40))
        restart = small_font.render("Press R to restart", True, WHITE)
        screen.blit(restart, (state.width // 2 - restart.get_width() // 2, state.height // 2 + 20))

    hint = small_font.render("W/S  vs  UP/DOWN", True, (150, 150, 150))
    screen.blit(hint, (state.width // 2 - hint.get_width() // 2, state.height - 25))

    pygame.display.flip()


def update_gameplay(state, pressed_keys):
    if pressed_keys[pygame.K_w]:
        state.left_paddle.move(-1, state.height)
    if pressed_keys[pygame.K_s]:
        state.left_paddle.move(1, state.height)

    if pressed_keys[pygame.K_UP]:
        state.right_paddle.move(-1, state.height)
    if pressed_keys[pygame.K_DOWN]:
        state.right_paddle.move(1, state.height)

    state.ball.rect.x += state.ball.vx
    state.ball.rect.y += state.ball.vy

    if state.ball.rect.top <= 0 or state.ball.rect.bottom >= state.height:
        state.ball.vy = -state.ball.vy

    if state.ball.rect.colliderect(state.left_paddle.rect) and state.ball.vx < 0:
        state.ball.rect.left = state.left_paddle.rect.right
        state.ball.vx = -state.ball.vx
    if state.ball.rect.colliderect(state.right_paddle.rect) and state.ball.vx > 0:
        state.ball.rect.right = state.right_paddle.rect.left
        state.ball.vx = -state.ball.vx

    if state.ball.rect.left <= 0:
        state.score[1] += 1
        state.ball.reset()
    elif state.ball.rect.right >= state.width:
        state.score[0] += 1
        state.ball.reset()


async def main():
    pygame.init()
    options = Options()
    screen = pygame.display.set_mode((options.width, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 48)
    small_font = pygame.font.SysFont("monospace", 20)

    phase = PHASE_MENU
    state = None
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if phase == PHASE_MENU:
                    if event.key == pygame.K_RETURN:
                        state = GameState(options.width, HEIGHT)
                        phase = PHASE_PLAYING
                    elif event.key == pygame.K_o:
                        phase = PHASE_OPTIONS
                elif phase == PHASE_OPTIONS:
                    if event.key == pygame.K_RETURN:
                        options.widescreen = not options.widescreen
                        screen = pygame.display.set_mode((options.width, HEIGHT))
                    elif event.key == pygame.K_ESCAPE:
                        phase = PHASE_MENU
                elif phase == PHASE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        phase = PHASE_MENU
                        state = None

        if phase == PHASE_PLAYING and state is not None:
            pressed_keys = pygame.key.get_pressed()
            winner = state.score[0] >= WINNING_SCORE or state.score[1] >= WINNING_SCORE

            if not winner:
                update_gameplay(state, pressed_keys)
            elif pressed_keys[pygame.K_r]:
                state.reset()

            draw_playing(screen, state, font, small_font)
        elif phase == PHASE_MENU:
            draw_menu(screen, options.width, HEIGHT, font, small_font)
        elif phase == PHASE_OPTIONS:
            draw_options(screen, options, options.width, HEIGHT, font, small_font)

        await asyncio.sleep(0)


asyncio.run(main())
