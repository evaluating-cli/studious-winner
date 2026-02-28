import platform
import sys

import pygame

if __package__ in (None, ""):
    from config import (
        BLACK,
        WHITE,
    )
else:
    from .config import (
        BLACK,
        WHITE,
    )

WINNING_SCORE_OPTIONS = [3, 5, 7, 10]
SPEED_OPTIONS = [180, 300, 420]
SPEED_LABELS = {180: "Slow", 300: "Normal", 420: "Fast"}


def handle_input(state, pressed_keys, dt):
    """Apply time-based paddle movement using dt in seconds."""
    paddle_delta = state.left_paddle.speed * dt

    if pressed_keys[pygame.K_w]:
        state.left_paddle.y_pos -= paddle_delta
    if pressed_keys[pygame.K_s]:
        state.left_paddle.y_pos += paddle_delta

    if pressed_keys[pygame.K_UP]:
        state.right_paddle.y_pos -= paddle_delta
    if pressed_keys[pygame.K_DOWN]:
        state.right_paddle.y_pos += paddle_delta

    state.left_paddle.y_pos = max(0.0, min(state.left_paddle.y_pos, state.height - state.left_paddle.rect.height))
    state.right_paddle.y_pos = max(
        0.0, min(state.right_paddle.y_pos, state.height - state.right_paddle.rect.height)
    )
    state.left_paddle.sync_rect()
    state.right_paddle.sync_rect()


def update_physics(state, dt):
    """Advance ball physics with time-based velocity (pixels/second)."""
    state.ball.x_pos += state.ball.vx * dt
    state.ball.y_pos += state.ball.vy * dt
    state.ball.sync_rect()

    if state.ball.rect.top <= 0:
        state.ball.y_pos = 0.0
        state.ball.vy = -state.ball.vy
        state.ball.sync_rect()
    elif state.ball.rect.bottom >= state.height:
        state.ball.y_pos = float(state.height - state.ball.rect.height)
        state.ball.vy = -state.ball.vy
        state.ball.sync_rect()


def resolve_collisions(state):
    if state.ball.rect.colliderect(state.left_paddle.rect) and state.ball.vx < 0:
        state.ball.rect.left = state.left_paddle.rect.right
        state.ball.x_pos = float(state.ball.rect.x)
        state.ball.vx = -state.ball.vx
    if state.ball.rect.colliderect(state.right_paddle.rect) and state.ball.vx > 0:
        state.ball.rect.right = state.right_paddle.rect.left
        state.ball.x_pos = float(state.ball.rect.x)
        state.ball.vx = -state.ball.vx


def update_scoring(state):
    if state.ball.rect.left <= 0:
        state.score[1] += 1
        state.ball.reset()
    elif state.ball.rect.right >= state.width:
        state.score[0] += 1
        state.ball.reset()


def draw_dashed_line(surface, color, start, end, dash_length=10):
    x1, y1 = start
    x2, y2 = end
    dy = y2 - y1
    dashes = dy // (dash_length * 2)
    for i in range(dashes):
        start_y = y1 + i * dash_length * 2
        end_y = start_y + dash_length
        pygame.draw.line(surface, color, (x1, start_y), (x2, end_y), 2)


def draw_start_screen(screen, fonts):
    font = fonts["font"]
    small_font = fonts["small_font"]
    width, height = screen.get_size()

    screen.fill(BLACK)

    title = font.render("PONG", True, WHITE)
    start = small_font.render("Press ENTER to start", True, WHITE)
    options_hint = small_font.render("Press O for options", True, (150, 150, 150))

    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 60))
    screen.blit(start, (width // 2 - start.get_width() // 2, height // 2 + 20))
    screen.blit(options_hint, (width // 2 - options_hint.get_width() // 2, height // 2 + 50))

    debug_color = (80, 80, 80)
    debug_line_height = 22
    py_ver = sys.version.split()[0]
    pg_ver = pygame.version.ver
    plat = platform.platform(terse=True)
    display_info = pygame.display.Info()
    debug_lines = [
        f"Python {py_ver} | pygame-ce {pg_ver}",
        f"Platform: {plat}",
        f"Display: {display_info.current_w}x{display_info.current_h} | Window: {width}x{height}",
    ]
    for i, line in enumerate(debug_lines):
        surf = small_font.render(line, True, debug_color)
        screen.blit(surf, (4, height - (len(debug_lines) - i) * debug_line_height))

    pygame.display.flip()


def draw_options_screen(screen, fonts, options, selected_index):
    font = fonts["font"]
    small_font = fonts["small_font"]
    width, height = screen.get_size()

    screen.fill(BLACK)

    title = font.render("OPTIONS", True, WHITE)
    screen.blit(title, (width // 2 - title.get_width() // 2, 60))

    items = [
        ("Winning Score", str(options.winning_score)),
        ("Ball Speed", SPEED_LABELS.get(options.ball_speed, str(options.ball_speed))),
        ("Paddle Speed", SPEED_LABELS.get(options.paddle_speed, str(options.paddle_speed))),
    ]

    for i, (label, value) in enumerate(items):
        color = WHITE if i == selected_index else (150, 150, 150)
        prefix = "> " if i == selected_index else "  "
        text = small_font.render(f"{prefix}{label}:  < {value} >", True, color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 40 + i * 50))

    hint = small_font.render(
        "UP/DOWN select   LEFT/RIGHT change   ESC confirm", True, (100, 100, 100)
    )
    screen.blit(hint, (width // 2 - hint.get_width() // 2, height - 30))

    pygame.display.flip()


def draw_frame(screen, state, fonts):
    font = fonts["font"]
    small_font = fonts["small_font"]
    width, height = screen.get_size()

    screen.fill(BLACK)

    draw_dashed_line(screen, WHITE, (width // 2, 0), (width // 2, height))

    pygame.draw.rect(screen, WHITE, state.left_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.right_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.ball.rect)

    left_score = font.render(str(state.score[0]), True, WHITE)
    right_score = font.render(str(state.score[1]), True, WHITE)
    screen.blit(left_score, (width // 4 - left_score.get_width() // 2, 20))
    screen.blit(right_score, (3 * width // 4 - right_score.get_width() // 2, 20))

    winner = None
    if state.score[0] >= state.winning_score:
        winner = "Left Player Wins!"
    elif state.score[1] >= state.winning_score:
        winner = "Right Player Wins!"

    if winner:
        msg = font.render(winner, True, WHITE)
        screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2 - 40))
        restart = small_font.render("R to restart  ·  Esc for menu", True, WHITE)
        screen.blit(restart, (width // 2 - restart.get_width() // 2, height // 2 + 20))

    hint = small_font.render("W/S  vs  UP/DOWN", True, (150, 150, 150))
    screen.blit(hint, (width // 2 - hint.get_width() // 2, height - 25))

    pygame.display.flip()
