import pygame
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Clash")

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100 , 80
BORDER = pygame.Rect( (WIDTH - 10) // 2, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load("assets/images/spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load("assets/images/spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (100, 80)),-90)

SPACE = pygame.transform.scale(pygame.image.load("assets/images/space.png"), (WIDTH, HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

HEALTH_FONT = pygame.font.SysFont(None, 40)
WINNER_FONT = pygame.font.SysFont(None, 100)
RESTART_FONT = pygame.font.SysFont(None, 50)

FIRE = pygame.mixer.Sound("assets/sound/Grenade+1.mp3")
BULLET_HIT = pygame.mixer.Sound("assets/sound/Gun+Silencer.mp3")
FIRE.set_volume(0.5)
BULLET_HIT.set_volume(0.6)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SHIP_VELOCITY = 8
BULLET_VELOCITY = 20
FPS = 60
OFFSET = 20
LEVEL = 5
DIFFICULTY = 3

has_frozen = False

def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    
    WIN.blit(red_text, (WIDTH - red_text.get_width() - 20, 20))
    WIN.blit(yellow_text, (20, 20))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()
    
def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - SHIP_VELOCITY > 0:
        yellow.x -= SHIP_VELOCITY
    if key_pressed[pygame.K_d] and yellow.x + SHIP_VELOCITY + yellow.width < BORDER.x:
        yellow.x += SHIP_VELOCITY
    if key_pressed[pygame.K_w] and yellow.y - SHIP_VELOCITY > 0:
        yellow.y -= SHIP_VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + SHIP_VELOCITY + yellow.height< HEIGHT - 20:
        yellow.y += SHIP_VELOCITY
        
def red_ai(red, yellow, red_bullets, yellow_bullets, frame_count, ai_state, red_health, yellow_health, time_elapsed):
    dodge_threshold = 200
    
    # -------- Dodging bullets -------- #
    danger_bullets = []
    for bullet in yellow_bullets:
        if red.x < bullet.x < red.x + 200:  # incoming bullets
            if abs(bullet.y - red.y) < red.height:
                danger_bullets.append(bullet)

    if frame_count % dodge_threshold == 0 and danger_bullets:
        # Decide direction
        if red.y + red.height // 2 < HEIGHT // 2:
            red.y += SHIP_VELOCITY
        else:
            red.y -= SHIP_VELOCITY
    
    # -------- Chasing Yellow -------- #
    if red.y + red.height // 2 < yellow.y + yellow.height // 2 and red.y + red.height < HEIGHT - 20:
        red.y += SHIP_VELOCITY - LEVEL + DIFFICULTY
    elif red.y + red.height // 2 > yellow.y + yellow.height // 2 and red.y > 0:
        red.y -= SHIP_VELOCITY - LEVEL + DIFFICULTY

    # -------- Shooting -------- #
    # ai_fire_counter += 1
    if time_elapsed > 0.5:
        ai_state["fire_counter"] += 1
        if ai_state["fire_counter"] >= 7:
            if abs(red.y - yellow.y) < 60 and len(red_bullets) < 4:
                bullet = pygame.Rect(red.x, red.y + red.height // 2, 20, 10)
                red_bullets.append(bullet)
                FIRE.play()
                # ai_fire_counter = 0
                ai_state["fire_counter"] = 0
            
    # --------Aggressive/Defensive -------- #
    aggressive = False
    STAGE = random.randint(600,WIDTH)
    
    if red_health > yellow_health and yellow_health < 10:
        aggressive = True
    
    if red.x > STAGE:
        red.x -= SHIP_VELOCITY - LEVEL
    if yellow.x == 0:
        red.x -= SHIP_VELOCITY - LEVEL
    elif not aggressive and red.x < 3 * WIDTH // 4 and red.x < STAGE:
        red.x += SHIP_VELOCITY - LEVEL
    elif (aggressive or yellow.x < WIDTH // 8) and red.x > BORDER.x + OFFSET:
        red.x -= SHIP_VELOCITY - LEVEL
        

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    
    r_pos_x = random.randint(BORDER.x,WIDTH - SPACESHIP_WIDTH - OFFSET)
    r_pos_y = random.randint(0,HEIGHT - SPACESHIP_HEIGHT - OFFSET)
    y_pos_x = random.randint(0,BORDER.x - SPACESHIP_WIDTH - OFFSET)
    y_pos_y = random.randint(0,HEIGHT - SPACESHIP_HEIGHT - OFFSET)
    
    red = pygame.Rect(r_pos_x, r_pos_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(y_pos_x, y_pos_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    clock = pygame.time.Clock()
    start_time = time.time()
    time_elapsed = 0
    
    run = True
    ai_state = {"fire_counter": 0}
    red_health = 15
    yellow_health = 15
    
    while run:
        clock.tick(FPS)
        frame_count = 0
        time_elapsed = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < 4:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 ,20, 10)
                    yellow_bullets.append(bullet)
                    FIRE.play()
                    
                if event.key == pygame.K_RETURN and len(red_bullets) < 4:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 ,20, 10)
                    red_bullets.append(bullet)
                    FIRE.play()
        
            winner_text = ""
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT.play()
                if yellow_health <= 0:
                    winner_text = "Red Wins!"
                    run = False
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()
                if red_health <= 0:
                    winner_text = "Yellow Wins!"
                    run = False
            
            if winner_text != "":
                draw_winner(winner_text)
                
        key_pressed = pygame.key.get_pressed()
        frame_count += 1
        yellow_movement(key_pressed, yellow)
        red_ai(red, yellow, red_bullets, yellow_bullets, frame_count, ai_state, red_health, yellow_health, time_elapsed)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)               
        draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    restart_text = RESTART_FONT.render("Press R to Restart or Q to Quit", 1, WHITE)
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))
    pygame.display.update()
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                
if __name__ == "__main__":
    main()