import asyncio

if __package__ in (None, ""):
    from game import main
else:
    from .game import main


if __name__ == "__main__":
    asyncio.run(main())
