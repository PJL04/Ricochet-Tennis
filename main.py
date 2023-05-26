import pygame, sys

# General setup
pygame.init()
clock = pygame.time.Clock()

# Window setup
screen_width = 1280
screen_height = 960
# Display as variable
screen = pygame.display.set_mode((screen_width,screen_height))
# Title
pygame.display.set_caption("Ricochet Tennis")


# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Background color
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)

ball_speed_x = 8
ball_speed_y = 8


def ball_movement():
    # need global variable because local variable "bal_speed_x referenced before assignment"
    global ball_speed_x, ball_speed_y
    # Ball gets speed
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball bounces off the edge of the screen
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball bounces off the player rect
    if ball.colliderect(player) or  ball.colliderect(opponent):
        ball_speed_x *= -1


# Game loop
while True:
    # Handling input
    # get user input
    for event in pygame.event.get():
        # if user clicks close
        if event.type == pygame.QUIT:
            # quitting game
            pygame.quit()
            # close window
            sys.exit

    ball_movement()

    # Drawings
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2,screen_height))
    


    # Updating the window
    pygame.display.flip()
    # Limits how fast the code runs (FPS)
    clock.tick(60)
