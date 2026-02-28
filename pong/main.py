import asyncio

if __package__ in (None, ""):
    from game import main
else:
    from .game import main

asyncio.run(main())
