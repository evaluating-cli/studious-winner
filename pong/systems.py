import pygame

if __package__ in (None, ""):
    from config import (
        BLACK,
        HEIGHT,
        WHITE,
        WIDTH,
        WINNING_SCORE,
    )
else:
    from .config import (
        BLACK,
        HEIGHT,
        WHITE,
        WIDTH,
        WINNING_SCORE,
    )


def handle_input(state, pressed_keys):
    if pressed_keys[pygame.K_w]:
        state.left_paddle.rect.y -= state.left_paddle.speed
    if pressed_keys[pygame.K_s]:
        state.left_paddle.rect.y += state.left_paddle.speed

    if pressed_keys[pygame.K_UP]:
        state.right_paddle.rect.y -= state.right_paddle.speed
    if pressed_keys[pygame.K_DOWN]:
        state.right_paddle.rect.y += state.right_paddle.speed

    state.left_paddle.rect.y = max(0, min(state.left_paddle.rect.y, HEIGHT - state.left_paddle.rect.height))
    state.right_paddle.rect.y = max(0, min(state.right_paddle.rect.y, HEIGHT - state.right_paddle.rect.height))


def update_physics(state, dt):  # dt intentionally unused to preserve frame-based behavior
    _ = dt
    state.ball.rect.x += state.ball.vx
    state.ball.rect.y += state.ball.vy
    if state.ball.rect.top <= 0 or state.ball.rect.bottom >= HEIGHT:
        state.ball.vy = -state.ball.vy


def resolve_collisions(state):
    if state.ball.rect.colliderect(state.left_paddle.rect) and state.ball.vx < 0:
        state.ball.rect.left = state.left_paddle.rect.right
        state.ball.vx = -state.ball.vx
    if state.ball.rect.colliderect(state.right_paddle.rect) and state.ball.vx > 0:
        state.ball.rect.right = state.right_paddle.rect.left
        state.ball.vx = -state.ball.vx


def update_scoring(state):
    if state.ball.rect.left <= 0:
        state.score[1] += 1
        state.ball.reset()
    elif state.ball.rect.right >= WIDTH:
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


def draw_frame(screen, state, fonts):
    font = fonts["font"]
    small_font = fonts["small_font"]

    screen.fill(BLACK)

    draw_dashed_line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    pygame.draw.rect(screen, WHITE, state.left_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.right_paddle.rect)
    pygame.draw.rect(screen, WHITE, state.ball.rect)

    left_score = font.render(str(state.score[0]), True, WHITE)
    right_score = font.render(str(state.score[1]), True, WHITE)
    screen.blit(left_score, (WIDTH // 4 - left_score.get_width() // 2, 20))
    screen.blit(right_score, (3 * WIDTH // 4 - right_score.get_width() // 2, 20))

    winner = None
    if state.score[0] >= WINNING_SCORE:
        winner = "Left Player Wins!"
    elif state.score[1] >= WINNING_SCORE:
        winner = "Right Player Wins!"

    if winner:
        msg = font.render(winner, True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
        restart = small_font.render("Press R to restart", True, WHITE)
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

    hint = small_font.render("W/S  vs  UP/DOWN", True, (150, 150, 150))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 25))

    pygame.display.flip()
