import pygame, sys, random


class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = "stopped"
        self.draw()

    def draw(self):
        pygame.draw.rect(
            self.screen, self.color, (self.posX, self.posY, self.width, self.height)
        )

    def move(self):
        # moving up
        if self.state == "up":
            self.posY -= 6

        # moving down
        elif self.state == "down":
            self.posY += 6

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.height >= HEIGHT:
            self.posY = HEIGHT - self.height

    def reset_pos(self):
        self.posY = HEIGHT // 2 - self.height // 2
        self.state = "stopped"
        self.draw()


class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.dx = 0
        self.dy = 0
        self.radius = radius
        self.draw()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start(self):

        x_value = [5, 7, -5, -7]
        y_value = [3, 5, 7, -3, -5, -7]
        self.dx = random.choice(x_value)
        self.dy = random.choice(y_value)

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def wall_collision(self):
        self.dy = -self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def reset_pos(self):
        self.posX = WIDTH // 2
        self.posY = HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.draw()


class PlayerScore:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("monospace", 60, bold=True)
        self.label = self.font.render(self.points, 0, WHITE)
        self.show()

    def show(self):
        self.screen.blit(
            self.label, (self.posX - self.label.get_rect().width // 2, self.posY)
        )

    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, WHITE)

    def restart(self):
        self.points = "0"
        self.label = self.font.render(self.points, 0, WHITE)


class CollisionManager:
    def between_ball_and_paddle_left(self, ball, paddle):
        ballX = ball.posX
        ballY = ball.posY
        paddleX = paddle.posX
        paddleY = paddle.posY

        # y condition
        if (
            ballY + ball.radius > paddleY
            and ballY - ball.radius < paddleY + paddle.height
        ):
            # x condition
            if ballX - ball.radius <= paddleX + paddle.width:
                # collision
                return True

        # no collision
        return False

    def between_ball_and_paddle_right(self, ball, paddle):
        ballX = ball.posX
        ballY = ball.posY
        paddleX = paddle.posX
        paddleY = paddle.posY

        # y condition
        if (
            ballY + ball.radius > paddleY
            and ballY - ball.radius < paddleY + paddle.height
        ):
            # x condition
            if ballX + ball.radius >= paddleX:
                # collision
                return True

        # no collision
        return False

    def between_ball_and_walls(self, ball):
        ballY = ball.posY

        # top collision
        if ballY - ball.radius <= 0:
            return True

        # bottom collision
        if ballY + ball.radius >= HEIGHT:
            return True

        # no collision
        return False

    def check_left_player_point(self, ball):
        return ball.posX - ball.radius >= WIDTH

    def check_right_player_point(self, ball):
        return ball.posX + ball.radius <= 0


# CONSTANTS

WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# SCREEN
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

# FUNCTIONS


def draw_board():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)


def restart():
    draw_board()
    score1.restart()
    score2.restart()
    ball.reset_pos()
    paddle_left.reset_pos()
    paddle_right.reset_pos()


draw_board()

# OBJECTS

paddle_left = Paddle(screen, WHITE, 15, HEIGHT // 2 - 60, 20, 120)
paddle_right = Paddle(screen, WHITE, WIDTH - 20 - 15, HEIGHT // 2 - 60, 20, 120)
ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 8)
collision = CollisionManager()
score1 = PlayerScore(screen, "0", WIDTH // 4, 10)
score2 = PlayerScore(screen, "0", WIDTH - WIDTH // 4, 10)

# VARIABLES

playing = False
clock = pygame.time.Clock()

# MAINLOOP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not playing:
                ball.start()
                playing = True

            if event.key == pygame.K_r and playing:
                restart()
                playing = False

            if event.key == pygame.K_w:
                paddle_left.state = "up"

            if event.key == pygame.K_s:
                paddle_left.state = "down"

            if event.key == pygame.K_UP:
                paddle_right.state = "up"

            if event.key == pygame.K_DOWN:
                paddle_right.state = "down"

        if event.type == pygame.KEYUP:
            paddle_left.state = "stopped"
            paddle_right.state = "stopped"

    if playing:
        draw_board()

        ball.move()
        ball.draw()

        paddle_left.move()
        paddle_left.clamp()
        paddle_left.draw()

        paddle_right.move()
        paddle_right.clamp()
        paddle_right.draw()

        # wall collision
        if collision.between_ball_and_walls(ball):

            ball.wall_collision()

        # paddle_left collision
        if collision.between_ball_and_paddle_left(ball, paddle_left):

            ball.paddle_collision()

        # paddle_right collision
        if collision.between_ball_and_paddle_right(ball, paddle_right):

            ball.paddle_collision()

        if collision.check_left_player_point(ball):
            draw_board()
            score1.increase()
            ball.reset_pos()
            paddle_left.reset_pos()
            paddle_right.reset_pos()
            playing = False

        if collision.check_right_player_point(ball):
            draw_board()
            score2.increase()
            ball.reset_pos()
            paddle_left.reset_pos()
            paddle_right.reset_pos()
            playing = False

    score1.show()
    score2.show()

    clock.tick(40)
    pygame.display.update()
