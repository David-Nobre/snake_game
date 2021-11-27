import pygame
import time
import random
import string
 
pygame.init()
 
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
COPPER = (184, 115, 51)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (50, 255, 70)
BLUE = (50, 153, 213)

CHARACTERS = set (string.ascii_letters + string.digits)
 
WIDTH = 800
HEIGHT = 600
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game!")
 
clock = pygame.time.Clock()
 
SNAKE_BLOCK = 10
SNAKE_SPEED = 20
 
FONT_STYLE = pygame.font.SysFont("comicsans", 25)
SCORE_FONT = pygame.font.SysFont("comicsans", 20)

def user_input (score):
    string = ""
    string_over = False
    SCREEN.fill(GREEN)
    draw_border()
    Your_score(score)
    draw_string("Your Name:", 50)
    pygame.display.update()
    while not string_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if len (string) == 15:
                    string_over = True
                elif event.key == pygame.K_RETURN:
                    string_over = True
                elif event.unicode in CHARACTERS:                      
                    string += event.unicode
                    SCREEN.fill(GREEN)
                    draw_border()
                    Your_score(score)
                    draw_string("Your Name:", 50)
                    draw_string(string, 0)
                    pygame.display.update()
    sorted_scores = sort_scores (string, score)
    save_score (sorted_scores)
 
def sort_scores (string, score):
    scores = [(string, score)]
    try:
        with open ("snake_leaderboard.txt", "r") as f:
            lines = f.readlines()
    except IOError: #file not found
        return scores
    for line in lines:
        name, score = line.replace ("\n", "").split("->")
        scores.append ((name, int (score)))
    scores.sort (key = lambda x:~x[1])
    return scores

def save_score (sorted_scores):
    with open ("snake_leaderboard.txt", "w") as f:
        for elem in sorted_scores:
            f.write (f"{elem[0]}->{elem[1]}\n")

def get_leaderboard ():
    scores = []
    try:
        with open ("snake_leaderboard.txt", "r") as f:
            lines = f.readlines()
    except IOError: #file not found
        return scores
    for line in lines:
        name, score = line.replace ("\n", "").split("->")
        scores.append ((name, int (score)))
    return scores

def display_leaderboard (score):
    checking_leaderboard = True
    scores = get_leaderboard()

    SCREEN.fill(GREEN)
    draw_border()
    Your_score (score)
    pygame.draw.rect (SCREEN, WHITE, [WIDTH//3, 40, WIDTH//3, HEIGHT - 50])
    if not scores:
        message("No scores found", 0, RED)
        pygame.display.update ()
        while checking_leaderboard:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        checking_leaderboard = False
        return

    line = FONT_STYLE.render ("LeaderBoard", True, BLACK)
    lenght_x = FONT_STYLE.size ("LeaderBoard")[0]
    SCREEN.blit (line, [(WIDTH - lenght_x)//2, HEIGHT // 12])
    for idx, score in enumerate (scores):
        if idx == 10:
            break
        line = FONT_STYLE.render (f"{score[0]}--->{score[1]}", True, get_color(idx + 1))
        lenght_x = FONT_STYLE.size (f"{score[0]}--->{score[1]}")[0]
        SCREEN.blit (line, [(WIDTH - lenght_x)//2, (HEIGHT *(idx + 2))// 12])
    pygame.display.update()
    while checking_leaderboard:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    checking_leaderboard = False

def get_color (pos):
    if pos == 1:
        return GOLD
    elif pos == 2:
        return SILVER
    elif pos == 3:
        return COPPER
    else: 
        return BLACK
    

def draw_string (string, height_displacement):
    your_name = FONT_STYLE.render (string, True, BLACK)
    lenght_x = FONT_STYLE.size (string)[0]
    SCREEN.blit (your_name, [(WIDTH - lenght_x)//2, (HEIGHT - height_displacement)//2])

def draw_border (): 
    for x in [0, WIDTH - SNAKE_BLOCK]:
        for y in range (30, HEIGHT, SNAKE_BLOCK):
            pygame.draw.rect(SCREEN, BLACK, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])
    for y in [30, HEIGHT - SNAKE_BLOCK]:
        for x in range (0, WIDTH, SNAKE_BLOCK):
            pygame.draw.rect(SCREEN, BLACK, [x, y, SNAKE_BLOCK, SNAKE_BLOCK])
    
    
def Your_score(score):
    value = SCORE_FONT.render(f"Your Score: {score}", True, BLACK)
    SCREEN.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(SCREEN, WHITE, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, displacement, color):
    mesg = FONT_STYLE.render(msg, True, color)
    lenght_x = FONT_STYLE.size (msg)[0]
    SCREEN.blit(mesg, [(WIDTH - lenght_x)// 2, (HEIGHT - displacement)//2])
 
 
def gameLoop():
    game_over = False
    game_close = False
    final_score = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(SNAKE_BLOCK, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(30 + SNAKE_BLOCK, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    last_action = ""
 
    while not game_over:

        while final_score:
            SCREEN.fill(GREEN)
            draw_border()
            our_snake(SNAKE_BLOCK, snake_List)
            Your_score(Length_of_snake - 1)
            message (f"You Lost! Your score was {Length_of_snake - 1}", 40, RED)
            message ("Press S-save, L-Leaderboard or C-continue", -10, RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        user_input(Length_of_snake - 1)
                        final_score = False
                        time.sleep (1)
                    elif event.key == pygame.K_c:
                        final_score = False
                    elif event.key == pygame.K_l:
                        display_leaderboard(Length_of_snake - 1)
 
        while game_close:
            SCREEN.fill(GREEN)
            draw_border()
            our_snake(SNAKE_BLOCK, snake_List)
            message("Press R-Re-play or Q-Quit", 0, RED)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if last_action != "RIGHT":
                        x1_change = -SNAKE_BLOCK
                        y1_change = 0
                        last_action = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    if last_action != "LEFT":
                        x1_change = SNAKE_BLOCK
                        y1_change = 0
                        last_action = "RIGHT"
                elif event.key == pygame.K_UP:
                    if last_action != "DOWN":
                        y1_change = -SNAKE_BLOCK
                        x1_change = 0
                        last_action = "UP"
                elif event.key == pygame.K_DOWN:
                    if last_action != "UP":
                        y1_change = SNAKE_BLOCK
                        x1_change = 0
                        last_action = "DOWN"
 

        x1 += x1_change
        y1 += y1_change
        if x1 > WIDTH - 2*SNAKE_BLOCK or x1 < SNAKE_BLOCK or y1 > HEIGHT - 2*SNAKE_BLOCK or y1 < 30 + SNAKE_BLOCK:
            game_close = True
            final_score = True
        SCREEN.fill(GREEN)
        draw_border ()
        pygame.draw.rect(SCREEN, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                final_score = True
 
        our_snake(SNAKE_BLOCK, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(SNAKE_BLOCK, WIDTH - 2*SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(30 + SNAKE_BLOCK, HEIGHT - 2*SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(SNAKE_SPEED)
 
    pygame.quit()
    quit()

def main ():
    gameLoop()

if __name__ == '__main__':
    main ()