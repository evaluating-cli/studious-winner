import asyncio

import pygame

if __package__ in (None, ""):
    from config import HEIGHT, WIDTH
    from game import run_game
else:
    from .config import HEIGHT, WIDTH
    from .game import run_game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
fonts = {
    "font": pygame.font.SysFont("monospace", 48),
    "small_font": pygame.font.SysFont("monospace", 20),
}


async def main():
    await run_game(screen, clock, fonts)


asyncio.run(main())
