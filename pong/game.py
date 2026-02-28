import asyncio

import pygame

from pong.config import FPS, HEIGHT, WIDTH, WINNING_SCORE
from pong.entities import GameState
from pong.systems import draw_frame, handle_input, resolve_collisions, update_physics, update_scoring


async def run_game(screen, clock, fonts):
    state = GameState()

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

        if (state.score[0] >= WINNING_SCORE or state.score[1] >= WINNING_SCORE) and pressed_keys[pygame.K_r]:
            state.reset()

        draw_frame(screen, state, fonts)
        await asyncio.sleep(0)


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    fonts = {
        "font": pygame.font.SysFont("monospace", 48),
        "small_font": pygame.font.SysFont("monospace", 20),
    }

    await run_game(screen, clock, fonts)


if __name__ == "__main__":
    asyncio.run(main())
