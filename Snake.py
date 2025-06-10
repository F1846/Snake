import pygame
import random
import sys
import os

pygame.init()



initial_width = 800
initial_height = 600

screen_width = initial_width
screen_height = initial_height

BLOCK_SIZE = 20          
HUD_HEIGHT = 60         
SNAKE_SIZE = 40

def update_dimensions(new_width, new_height):
    global screen_width, screen_height, cols, rows, game_width, game_height, offset_x, offset_y
    screen_width, screen_height = new_width, new_height
    cols = screen_width // BLOCK_SIZE
    rows = (screen_height - HUD_HEIGHT) // BLOCK_SIZE
    game_width = cols * BLOCK_SIZE
    game_height = rows * BLOCK_SIZE
    offset_x = (screen_width - game_width) // 2  # Center game area horizontally
    offset_y = HUD_HEIGHT  # Game area starts just below the HUD

update_dimensions(initial_width, initial_height)


BACKGROUND_COLORS = [
    (64, 64, 64),         # Dark Gray
    (0, 255, 0),          # Green
    (0, 0, 255),          # Blue
    (255, 255, 0),        # Yellow
    (0, 255, 255),        # Cyan
    (255, 0, 255),        # Magenta
    (0, 0, 0),      # black
    (64, 64, 64),         # Dark Gray
    (139, 0, 0),          # Dark Red
    (0, 100, 0),          # Dark Green
    (0, 0, 139),          # Dark Blue
    (204, 204, 0),        # Dark Yellow
    (255, 182, 193),      # Pastel Pink
    (174, 198, 207),      # Pastel Blue
    (221, 160, 221),      # Pastel Purple
    (119, 221, 119),      # Pastel Green
    (255, 182, 193),      # Pastel Pink
    (174, 198, 207),      # Pastel Blue
    (221, 160, 221),      # Pastel Purple
    (119, 221, 119),      # Pastel Green
    (255, 105, 180),      # Pink
    (128, 0, 128),        # Purple
    (173, 216, 230),      # Light Blue
    (255, 99, 71),        # Tomato (a reddish-orange)
    (0, 255, 0),          # Lime Green
    (75, 0, 130),         # Indigo
    (238, 130, 238),      # Violet
    (64, 224, 208),       # Turquoise
]
bg_color_index = 0  # start with first color

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

COLOR_HUD_BG    = (0, 0, 0)
COLOR_HUD_TEXT  = (240, 240, 240)
COLOR_BORDER    = (255, 255, 255)

COLOR_SNAKE_BODY = (255, 140, 0)
COLOR_SNAKE_HEAD = (255, 140, 0)

COLOR_FOOD = (255, 0, 0)

# Fonts
hud_font           = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
menu_title_font    = pygame.font.SysFont("Comic Sans MS", 72, bold=True)
menu_button_font   = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
game_over_font     = pygame.font.SysFont("Comic Sans MS", 72, bold=True)
food_font          = pygame.font.SysFont("Comic Sans MS", 28, bold=True)

INITIAL_SPEED = 4   # Starting speed (frames per second)
clock = pygame.time.Clock()

HIGH_SCORE_FILE = "Score.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    else:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))



def draw_hud(score, lives, speed):
    pygame.draw.rect(dis, COLOR_HUD_BG, (0, 0, screen_width, HUD_HEIGHT))
    score_text = hud_font.render(f"Points: {score}", True, COLOR_HUD_TEXT)
    lives_text = hud_font.render(f"Vite: {lives}", True, COLOR_HUD_TEXT)
    speed_text = hud_font.render(f"Speed: {speed}", True, COLOR_HUD_TEXT)
    dis.blit(score_text, (20, 10))
    dis.blit(lives_text, (screen_width // 2 - 70, 10))
    dis.blit(speed_text, (screen_width - 200, 10))

def draw_snake(snake):
    for i, (col, row) in enumerate(snake):
        x = offset_x + col * BLOCK_SIZE
        y = offset_y + row * BLOCK_SIZE
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        if i == len(snake) - 1:
            pygame.draw.rect(dis, COLOR_SNAKE_HEAD, rect)
            
        else:
            pygame.draw.rect(dis, COLOR_SNAKE_BODY, rect)

def draw_food(food_pos):
    col, row = food_pos
    x = offset_x + col * BLOCK_SIZE
    y = offset_y + row * BLOCK_SIZE
    food_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(dis, COLOR_FOOD, food_rect)
    pygame.draw.rect(dis, COLOR_BORDER, food_rect, 2)
    letter = food_font.render("", True, COLOR_BORDER)
    letter_rect = letter.get_rect(center=food_rect.center)
    dis.blit(letter, letter_rect)

def draw_game_over():
    over_text = game_over_font.render("Game Over", True, WHITE)
    instr_text = menu_button_font.render("Press R to restart or Q to Quit", True, WHITE)
    over_rect = over_text.get_rect(center=(screen_width//2, screen_height//2 - 30))
    instr_rect = instr_text.get_rect(center=(screen_width//2, screen_height//2 + 30))
    dis.blit(over_text, over_rect)
    dis.blit(instr_text, instr_rect)

def draw_pause_menu():
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    dis.blit(overlay, (0, 0))
    pause_text = menu_title_font.render("Pause", True,  WHITE)
    resume_text = menu_button_font.render("Play", True, WHITE)
    exit_text = menu_button_font.render("Exit", True, WHITE)
    pause_rect = pause_text.get_rect(center=(screen_width//2, screen_height//2 - 100))
    resume_rect = pygame.Rect(0, 0, 250, 60)
    resume_rect.center = (screen_width//2, screen_height//2 - 20)
    exit_rect = pygame.Rect(0, 0, 250, 60)
    exit_rect.center = (screen_width//2, screen_height//2 + 60)
    pygame.draw.rect(dis, COLOR_HUD_BG, resume_rect)
    pygame.draw.rect(dis, COLOR_HUD_BG, exit_rect)
    pygame.draw.rect(dis, COLOR_BORDER, resume_rect, 2)
    pygame.draw.rect(dis, COLOR_BORDER, exit_rect, 2)
    dis.blit(pause_text, pause_rect)
    res_text_rect = resume_text.get_rect(center=resume_rect.center)
    exit_text_rect = exit_text.get_rect(center=exit_rect.center)
    dis.blit(resume_text, res_text_rect)
    dis.blit(exit_text, exit_text_rect)
    pygame.display.update()
    return resume_rect, exit_rect

def draw_menu():
    dis.fill(BACKGROUND_COLORS[bg_color_index])  
    title = menu_title_font.render(" Snake", True, COLOR_HUD_TEXT)
    play_text = menu_button_font.render("Play", True, WHITE)
    high_text = menu_button_font.render("High Score: " + str(load_high_score()), True, WHITE)
    exit_text = menu_button_font.render("Exit", True, WHITE)
    
    title_rect = title.get_rect(center=(screen_width//2, screen_height//2 - 150))
    play_rect = pygame.Rect(0, 0, 250, 60)
    play_rect.center = (screen_width//2, screen_height//2 - 30)
    high_rect = pygame.Rect(0, 0, 300, 60)
    high_rect.center = (screen_width//2, screen_height//2 + 40)
    exit_rect = pygame.Rect(0, 0, 250, 60)
    exit_rect.center = (screen_width//2, screen_height//2 + 120)
    
    pygame.draw.rect(dis, COLOR_HUD_BG, play_rect)
    pygame.draw.rect(dis, COLOR_HUD_BG, high_rect)
    pygame.draw.rect(dis, COLOR_HUD_BG, exit_rect)
    pygame.draw.rect(dis, COLOR_BORDER, play_rect, 2)
    pygame.draw.rect(dis, COLOR_BORDER, high_rect, 2)
    pygame.draw.rect(dis, COLOR_BORDER, exit_rect, 2)
    
    dis.blit(title, title_rect)
    dis.blit(play_text, play_text.get_rect(center=play_rect.center))
    dis.blit(high_text, high_text.get_rect(center=high_rect.center))
    dis.blit(exit_text, exit_text.get_rect(center=exit_rect.center))
    
    pygame.display.update()
    return play_rect, high_rect, exit_rect


def spawn_food(is_large=False):
    food_col = random.randint(0, cols - 1)
    food_row = random.randint(0, rows - 1)
    if is_large:
        return (food_col, food_row, True)  # bonus food: flag True
    else:
        return (food_col, food_row)  # normal food: 2-tuple



def main_menu():
    while True:
        play_button, _, exit_button = draw_menu()
        for event in pygame.event.get():
            # Allow window resize events.
            if event.type == pygame.VIDEORESIZE:
                update_dimensions(event.w, event.h)
                pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint(mx, my):
                    return
                elif exit_button.collidepoint(mx, my):
                    pygame.quit(); sys.exit()



def pause_menu():
    paused = True
    resume_button, exit_button = draw_pause_menu()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                update_dimensions(event.w, event.h)
                pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                # Redraw pause menu after resize.
                resume_button, exit_button = draw_pause_menu()
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if resume_button.collidepoint(mx, my):
                    paused = False
                elif exit_button.collidepoint(mx, my):
                    pygame.quit(); sys.exit()
        clock.tick(15)
    return



def game_loop():
    global dis, bg_color_index
    lives = 3
    score = 0
    speed = INITIAL_SPEED

    snake = [(cols // 2, rows // 2)]
    snake_length = 1
    dx, dy = 0, 0

    food_pos = spawn_food()  # Normal food at first
    large_food = None  # Variable to track large food

    checkpoint = {
        "snake": list(snake),
        "snake_length": snake_length,
        "dx": dx, "dy": dy,
        "score": score,
        "speed": speed,
    }

    game_over = False
    lost_life_message = False
    lost_life_counter = 0

    high_score = load_high_score()

    while True:
        # Handle window resize events.
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                update_dimensions(event.w, event.h)
                dis = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    pause_menu()
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1

        # Update snake position.
        head_col, head_row = snake[-1]
        new_col = (head_col + dx) % cols
        new_row = (head_row + dy) % rows
        new_head = (new_col, new_row)
        snake.append(new_head)
        if len(snake) > snake_length:
            snake.pop(0)

        dis.fill(BACKGROUND_COLORS[bg_color_index])
        draw_hud(score, lives, speed)
        draw_food(food_pos)
        if large_food:
            # Draw large food here
            draw_food(large_food[:2])  # Use only the position part of large food
        draw_snake(snake)
        if lost_life_message:
            msg = menu_button_font.render("Rimagnato!", True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(screen_width//2, screen_height//2))
            dis.blit(msg, msg_rect)
        pygame.display.update()

        # Check food collision.
        if new_head == food_pos:
            snake_length += 4  # Grow by 4 segments.
            score += 1
            if score % 6 == 0:
                speed += 1  # Increase speed every 4 foods eaten.
            if score % 40 == 0:
                speed -= 3
               
            if score % 40 == 0:  
                      snake_length = snake_length // 2
            if score % 50 == 0:
                large_food = spawn_food(is_large=True)
                score += 15  # Add 15 points for the large food
                food_pos = spawn_food() 
            else:
                food_pos = spawn_food()  

            # Change background color every x foods eaten.
            if score % 20000 == 0:
                bg_color_index = (bg_color_index + 1) % len(BACKGROUND_COLORS)
            checkpoint = {
                "snake": list(snake),
                "snake_length": snake_length,
                "dx": dx, "dy": dy,
                "score": score,
                "speed": speed,
            }

        # Self-collision.
        if new_head in snake[:-1]:
            lives -= 1
            if lives > 0:
                lost_life_message = True
                lost_life_counter = 30
                snake = list(checkpoint["snake"])
                snake_length = checkpoint["snake_length"]
                dx = checkpoint["dx"]
                dy = checkpoint["dy"]
                score = checkpoint["score"]
                speed = checkpoint["speed"]
                pygame.time.delay(1000)
            else:
                game_over = True

        if lost_life_message:
            lost_life_counter -= 1
            if lost_life_counter <= 0:
                lost_life_message = False

        if game_over:
            if score > high_score:
                save_high_score(score)
            dis.fill(BACKGROUND_COLORS[bg_color_index])
            draw_game_over()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                    elif event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
            continue

        clock.tick(speed)


dis = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption(" Snake")
main_menu()
game_loop()
