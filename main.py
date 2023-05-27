import pygame, sys
import random

# General setup
# Change buffer of sound
pygame.mixer.pre_init(44100, -16, 2, 512)
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
ball_color = (255, 255, 0)

ball_speed_x = 8 * random.choice((1, -1))
ball_speed_y = 8 * random.choice((1, -1))
player_speed = 0
opponent_speed = 8

# Text (score)
player_score = 0
opponent_score = 0
font = pygame.font.SysFont("impact", 32)

# Timer
score_time = True

# Sound
hit_sound = pygame.mixer.Sound("hit_new.ogg")
score_sound = pygame.mixer.Sound("score_new.ogg")
wall_sound = pygame.mixer.Sound("wall_new.ogg")
# Sound volume
score_sound.set_volume(0.1)
hit_sound.set_volume(0.2)
wall_sound.set_volume(0.2)

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()

    ball.center = (screen_width/2, screen_height/2)

    # Display timer
    if current_time - score_time < 500:
        number_three = font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    
    if 500 < current_time - score_time < 1000:
        number_two = font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))

    if 1000 < current_time - score_time < 1500:
        number_one = font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 1500:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 8 * random.choice((1, -1))
        ball_speed_x = 8 * random.choice((1, -1))
        score_time = None

def ball_movement():
    # Need global variable because local variable "bal_speed_x referenced before assignment"
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    # Ball gets speed
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball bounces off the edge of the screen
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(wall_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        # Player scored
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        # Opponent scored
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # Ball bounces off the player rect
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(hit_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(hit_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_border():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_border():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def opponent_movement():
    # If opponent over ball move down; If oppoent is under ball move up
    if opponent.top < ball.y:
        opponent.top += opponent_speed 
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed


# Game loop
while True:
    # Handling input
    # Get user input
    for event in pygame.event.get():

        # If user clicks close
        if event.type == pygame.QUIT:
            # quitting game
            pygame.quit()
            # close window
            sys.exit

        # Player movement
        # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7

        # Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Logic
    ball_movement()
    player.y += player_speed
    player_border()
    opponent_border()
    opponent_movement()


    # Drawings
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2,screen_height))
    
    if score_time:
        pygame.mixer.Sound.play(score_sound)
        ball_restart()

    # Surface for player score
    player_text = font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 470))
    # Surface for opponent score
    opponent_text = font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 470))


    # Updating the window
    pygame.display.flip()
    # Limits how fast the code runs (FPS)
    clock.tick(60)
