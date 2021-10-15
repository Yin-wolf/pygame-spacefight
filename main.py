import pygame
import os  # OS
pygame.font.init()  # FONT INITAILIZE
pygame.mixer.init()  # SOUND INITAILIZE

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# CONSTANT VALUES

# GAME NAME
pygame.display.set_caption("Spacegame")

# COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# FONT
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# SOUND -- add your own sound files in Assets then call them
# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
# BULLET_FIRE_SOUNND = pygame.mixer.Sound(
#     os.path.join('Assets','Gun+Silencer.mp3'))

# Stablise Frames Per Second
FPS = 60

# VELOCITY, Rate of movement
VEL = 5

# BULLET VELOCITY
BULLET_VEL = 7

# BULLET AMOUNT / TIME
MAX_BULLETS = 3

# WIDTH, HEIGHT - IMAGE
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# CENTER BORDER
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# USEREVENT CREATE & ASSIGN UNIQUE ID
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# IMPORT ASSETS

"""
Images
    # Loading
    # Scaling WIDTH, HEIGHT
    # Rotating
"""

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')
), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    Giving color inside the Window, you can pass the (R, G, B) in it, 
    But the display won't be updates unless its manually updates.

    blit - drawing a surface on screen and make sure it is within the 
    dimensions of the WIDTH and HEIGHT

    In pygame the co-ordinate system start from top-left corner

    Here, stack structure is followed, so keep components in sequence
    """
    # WIN.fill(WHITE) # BACKGROUND COLOR
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # HEALTH LABEL
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    # HEALTH POSITION
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # SPACESHIP POSITION
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # DRAWING BULLETS
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()  # DISPLAY: MANUAL UPDATE


def yellow_handler(keys_pressed, yellow):
    """
    yellow.x should not be less than 0, 
    as the object will move out of screen
    that's why we are checking if Objects co-ordinate greater than 0
    """
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT, K_a: keyboard Key A
        yellow.x -= VEL

    """
    yellow.x should not be greater than Border, 
    So that object will not move out of its area
    that's why we are checking if Objects width doesn't cross the BORDER
    """
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT, K_d: keyboard Key D
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP, K_w: keyboard Key W
        yellow.y -= VEL
    # DOWN, K_s: keyboard Key S
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def red_handler(keys_pressed, red):
    # LEFT, K_LEFT: keyboard Key LEFT
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    # RIGHT, K_RIGHT: keyboard Key RIGHT
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP, K_UP: keyboard Key UP
        red.y -= VEL
    # DOWN, K_DOWN: keyboard Key DOWN
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


# REMOVE BULLETS, BULLET COLLISION, BULLET MOVEMENT
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # COLLISION CHECK: YELLOW BULLET (T / F)
            # an event to notify main() that YELLOW bullet has hit
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        # to check if bullets are going off the screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # COLLISION CHECK: RED BULLET
            # an event to notify main() that RED bullet has hit
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() //
             2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)  # DELAY: 5 sec (time x 1000)


def main():  # MAIN FUNCTION.

    # Creating a Rect of an entity by passing (x, y, w, h)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    # SPACESHIP HEALTH
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()

    run = True
    while run:
        """ 
        Main game loop that handles updating scores and etc 
        """

        # CLOCK RATE SETTING
        clock.tick(FPS)

        # EVENT OCCURANCE CHECK, for eg. bullet hit
        for event in pygame.event.get():

            # Here the while loop will end and the game will stop
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # BULLET LAUNCH & POSITION
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Bullet comes from middle of spaceship
                    bullet = pygame.Rect(
                        yellow.x + yellow.width - 2, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUNND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # Bullet comes from middle of spaceship
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUNND.play()

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        # HEALTH CHECK & WINNER DISPLAY
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # red.x += 1 -- to check the movement.

        # checking the pressed keys
        keys_pressed = pygame.key.get_pressed()
        yellow_handler(keys_pressed, yellow)
        red_handler(keys_pressed, red)

        # print(red_bullets, yellow_bullets)

        # function to check bullets hit the spaceship
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Calling the draw function, passing the red/yellow for position
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    # Stops the pygame itself
    # pygame.quit()

    # Restarts
    main()


if __name__ == "__main__":
    while True:
        main()
