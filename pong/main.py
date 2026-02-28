import asyncio
import sys

import pygame

from .config import FPS, HEIGHT, WIDTH
from .entities import GameState, Options
from .systems import (
    SPEED_OPTIONS,
    WINNING_SCORE_OPTIONS,
    draw_frame,
    draw_options_screen,
    draw_start_screen,
    handle_input,
    resolve_collisions,
    update_physics,
    update_scoring,
)


async def run_start_screen(screen, clock, fonts):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                if event.key == pygame.K_o:
                    return "options"
        draw_start_screen(screen, fonts)
        await asyncio.sleep(0)


def _cycle_option(options_list, current, delta, default_idx=0):
    idx = options_list.index(current) if current in options_list else default_idx
    return options_list[(idx + delta) % len(options_list)]


async def run_options_screen(screen, clock, fonts, options):
    selected = 0
    num_items = 3
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    running = False
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % num_items
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % num_items
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    delta = -1 if event.key == pygame.K_LEFT else 1
                    if selected == 0:
                        options.winning_score = _cycle_option(WINNING_SCORE_OPTIONS, options.winning_score, delta)
                    elif selected == 1:
                        options.ball_speed = _cycle_option(SPEED_OPTIONS, options.ball_speed, delta, 1)
                    elif selected == 2:
                        options.paddle_speed = _cycle_option(SPEED_OPTIONS, options.paddle_speed, delta, 1)
        draw_options_screen(screen, fonts, options, selected)
        await asyncio.sleep(0)
    return True


async def run_game(screen, clock, fonts, options):
    width, height = screen.get_size()
    state = GameState(width, height, options)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        handle_input(state, pressed_keys)

        update_physics(state, dt)
        resolve_collisions(state)
        update_scoring(state)

        game_over = state.score[0] >= state.winning_score or state.score[1] >= state.winning_score
        if game_over and pressed_keys[pygame.K_r]:
            state.reset()

        draw_frame(screen, state, fonts)
        await asyncio.sleep(0)


async def main():
    pygame.init()
    if sys.platform == "emscripten":
        screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    fonts = {
        "font": pygame.font.SysFont("monospace", 48),
        "small_font": pygame.font.SysFont("monospace", 20),
    }

    options = Options()
    while True:
        result = await run_start_screen(screen, clock, fonts)
        if not result:
            break
        if result == "options":
            if not await run_options_screen(screen, clock, fonts, options):
                break
            continue
        await run_game(screen, clock, fonts, options)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
