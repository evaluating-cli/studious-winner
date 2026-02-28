WIDTH, HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 15
FPS = 60
WINNING_SCORE = 7

LEFT_PADDLE_X = 20
PADDLE_START_Y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Time-based movement model:
# speeds are measured in pixels per second and multiplied by dt (seconds).
PADDLE_SPEED = 360
BALL_SPEED_X = 300
