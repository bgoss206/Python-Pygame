import pygame
import os 
pygame.font.init()

WIDTH, HEIGHT = 1000, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starfighting!")

WHITE = (255, 255, 255)
BORDER_RGB = (186, 234, 243)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (60, 50)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Pygame_Tutorial', 'space.png')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame_Tutorial', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame_Tutorial','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BORDER_RGB, BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (10,10))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)        
        
    pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)    
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)

def handle_red_movement(keys_pressed, red):
    if (keys_pressed[pygame.K_a] and red.x - VEL > 0): #left
        red.x -= VEL
    if (keys_pressed[pygame.K_d] and red.x + VEL + (red.width/1.5) < BORDER.x): #right
        red.x += VEL
    if (keys_pressed[pygame.K_w] and red.y - VEL > 0): #up
        red.y -= VEL
    if (keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT): #down
        red.y += VEL

def handle_yellow_movement(keys_pressed, yellow):
    if (keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x): #left
        yellow.x -= VEL
    if (keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH): #right
        yellow.x += VEL
    if (keys_pressed[pygame.K_UP] and yellow.y - VEL > 0): #up
        yellow.y -= VEL
    if (keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT): #down
        yellow.y += VEL


def handle_button_press(pressed_x, pressed_y, button):
    return ((pressed_x > button.x) & (pressed_x < button.x + button.width) & (pressed_y < button.y + button.height) & (pressed_y > button.y))

def main():

    red = pygame.Rect(200, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(750, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    CLOCK = pygame.time.Clock()
    run = True
    while (run):
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                          
            
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1


            
        keys_pressed = pygame.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_yellow_movement(keys_pressed, yellow)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
            WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
            pygame.display.update()     



    main()



if __name__ == "__main__":
    main()
