import asyncio
import pygame

# Constants
NORMAL_WIDTH, HEIGHT = 640, 480
WIDESCREEN_WIDTH = 854
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 15
FPS = 60
WINNING_SCORE = 7

# Game phases
PHASE_MENU = "menu"
PHASE_OPTIONS = "options"
PHASE_PLAYING = "playing"


class Options:
    def __init__(self):
        self.widescreen = False

    @property
    def width(self):
        return WIDESCREEN_WIDTH if self.widescreen else NORMAL_WIDTH


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 6

    def move(self, up_key, down_key, height):
        keys = pygame.key.get_pressed()
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed
        self.rect.y = max(0, min(self.rect.y, height - PADDLE_HEIGHT))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            self.width // 2 - BALL_SIZE // 2,
            self.height // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.vx = 5
        self.vy = 5

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top <= 0 or self.rect.bottom >= self.height:
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
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left_paddle = Paddle(20, height // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(width - 30, height // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(width, height)
        self.score = [0, 0]

    def reset(self):
        self.left_paddle = Paddle(20, self.height // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(self.width - 30, self.height // 2 - PADDLE_HEIGHT // 2)
        self.ball.reset()
        self.score = [0, 0]


def draw_menu(surface, width, height):
    surface.fill(BLACK)
    title = font.render("PONG", True, WHITE)
    surface.blit(title, (width // 2 - title.get_width() // 2, height // 4))
    play_text = font.render("Play", True, WHITE)
    surface.blit(play_text, (width // 2 - play_text.get_width() // 2, height // 2))
    options_text = small_font.render("Options  (O)", True, GRAY)
    surface.blit(options_text, (width // 2 - options_text.get_width() // 2, height // 2 + 70))
    hint = small_font.render("ENTER - Play  |  O - Options", True, GRAY)
    surface.blit(hint, (width // 2 - hint.get_width() // 2, height - 30))


def draw_options(surface, width, height, opts):
    surface.fill(BLACK)
    title = font.render("Options", True, WHITE)
    surface.blit(title, (width // 2 - title.get_width() // 2, height // 6))
    ws_label = "Widescreen:  " + ("ON " if opts.widescreen else "OFF")
    ws_color = WHITE if opts.widescreen else GRAY
    ws_text = font.render(ws_label, True, ws_color)
    surface.blit(ws_text, (width // 2 - ws_text.get_width() // 2, height // 2 - 24))
    hint = small_font.render("ENTER - Toggle Widescreen  |  ESC - Back", True, GRAY)
    surface.blit(hint, (width // 2 - hint.get_width() // 2, height - 30))


pygame.init()
options = Options()
screen = pygame.display.set_mode((options.width, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 48)
small_font = pygame.font.SysFont("monospace", 20)


async def main():
    global screen

    phase = PHASE_MENU
    state = GameState(options.width, HEIGHT)

    running = True
    while running:
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
                    if event.key == pygame.K_ESCAPE:
                        phase = PHASE_MENU
                    elif event.key == pygame.K_RETURN:
                        options.widescreen = not options.widescreen
                        screen = pygame.display.set_mode((options.width, HEIGHT))
                elif phase == PHASE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        phase = PHASE_MENU

        if phase == PHASE_MENU:
            draw_menu(screen, options.width, HEIGHT)

        elif phase == PHASE_OPTIONS:
            draw_options(screen, options.width, HEIGHT, options)

        elif phase == PHASE_PLAYING:
            screen.fill(BLACK)

            state.left_paddle.move(pygame.K_w, pygame.K_s, HEIGHT)
            state.right_paddle.move(pygame.K_UP, pygame.K_DOWN, HEIGHT)

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
            elif state.ball.rect.right >= state.width:
                state.score[0] += 1
                state.ball.reset()

            # Draw center line
            draw_dashed_line(screen, WHITE, (state.width // 2, 0), (state.width // 2, HEIGHT))

            # Draw paddles and ball
            state.left_paddle.draw(screen)
            state.right_paddle.draw(screen)
            state.ball.draw(screen)

            # Draw scores
            left_score = font.render(str(state.score[0]), True, WHITE)
            right_score = font.render(str(state.score[1]), True, WHITE)
            screen.blit(left_score, (state.width // 4 - left_score.get_width() // 2, 20))
            screen.blit(right_score, (3 * state.width // 4 - right_score.get_width() // 2, 20))

            # Win condition
            winner = None
            if state.score[0] >= WINNING_SCORE:
                winner = "Left Player Wins!"
            elif state.score[1] >= WINNING_SCORE:
                winner = "Right Player Wins!"

            if winner:
                msg = font.render(winner, True, WHITE)
                screen.blit(msg, (state.width // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
                restart = small_font.render("Press R to restart", True, WHITE)
                screen.blit(restart, (state.width // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    state.reset()

            # Controls hint
            hint = small_font.render("W/S  vs  UP/DOWN  |  ESC - Menu", True, GRAY)
            screen.blit(hint, (state.width // 2 - hint.get_width() // 2, HEIGHT - 25))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())
