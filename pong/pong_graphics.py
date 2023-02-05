import pong
import pygame
import time

def game(game_screen, game_type=1):#1. network vs player, 2. player vs player, 3. network vs network
    env = pong.Env()
    fps = 60
    env.new_game()
    running = True
    while env.paddle1.score < 10 and env.paddle2.score < 10 and running:
        frame_time = time.time()
        draw(env, game_screen)
        env.update_env(game_type)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if game_type != 3:
            if keys[pygame.K_DOWN]:
                env.paddle2.action(2)
            if keys[pygame.K_UP]:
                env.paddle2.action(0)
        if game_type == 2:
            if keys[pygame.K_s]:
                env.paddle1.action(2)
            if keys[pygame.K_w]:
                env.paddle1.action(0)
        if 1/fps - time.time() + frame_time > 0.001:
            time.sleep(1/fps - time.time() + frame_time)
    if env.paddle1.score == 10:
        draw(env, game_screen)
        winning_screen(game_screen, env, game_type)
        pygame.display.flip()
    else:
        draw(env, game_screen)
        winning_screen(game_screen, env, game_type)
        pygame.display.flip()

def restart_button(game_screen, game_type):
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(150, 400, 200, 100))
    display(game_screen, (170, 415), "restart", color=(0, 255, 0))
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(450, 400, 200, 100))
    display(game_screen, (490, 415), "menu", color=(0, 255, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > 150 and mouse[0] < 350 and mouse[1] > 400 and mouse[1] < 500:
                    game(game_screen, game_type)
                    running = False #we want the program to quit if we didnt choose restart or menu in the end of the match
                if mouse[0] > 450 and mouse[0] < 650 and mouse[1] > 400 and mouse[1] < 500:
                    menu()
                    running = False #we want the program to quit if we didnt choose restart or menu in the end of the match

def menu():
    pygame.init()
    game_screen = pygame.display.set_mode((800, 600))
    display(game_screen, (330, 0), "menu:", color=(0, 255, 0))
    pygame.display.set_caption('pong')
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(200, 120, 400, 100))
    display(game_screen, (210, 135), "player vs player", color=(0, 255, 0))
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(200, 270, 400, 100))
    display(game_screen, (210, 285), "ai vs player", color=(0, 255, 0))
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(200, 420, 400, 100))
    display(game_screen, (210, 435), "ai vs ai", color=(0, 255, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > 200 and mouse[0] < 600 and mouse[1] > 120 and mouse[1] < 220:
                    game(game_screen, 2)
                    running = False #we want the program to quit if we didnt choose restart or menu in the end of the match
                if mouse[0] > 200 and mouse[0] < 600 and mouse[1] > 270 and mouse[1] < 370:
                    game(game_screen, 1)
                    running = False #we want the program to quit if we didnt choose restart or menu in the end of the match
                if mouse[0] > 200 and mouse[0] < 600 and mouse[1] > 420 and mouse[1] < 520:
                    game(game_screen, 3)
                    running = False #we want the program to quit if we didnt choose restart or menu in the end of the match

def winning_screen(game_screen, env, game_type):
    if env.paddle1.score > env.paddle2.score:
        display(game_screen, (220, 250), "left paddle won!")
    elif env.paddle1.score < env.paddle2.score:
        display(game_screen, (200, 250), "right paddle won!")
    else:
        display(game_screen, (300, 250), "Its a tie!")
    restart_button(game_screen, game_type)

def draw(env, game_screen):
    game_screen.fill((0, 0, 0))
    pygame.draw.line(game_screen, (100, 100, 100), (env.screen[0] // 2, 0), (env.screen[0] // 2, env.screen[1]), 2)
    display(game_screen, (310, 20), env.paddle1.score)
    display(game_screen, (460, 20), env.paddle2.score)
    env.paddle1.update_rect()
    env.paddle2.update_rect()
    pygame.draw.rect(game_screen, (255, 255, 255), env.paddle1.rect)
    pygame.draw.rect(game_screen, (255, 255, 255), env.paddle2.rect)
    pygame.draw.circle(game_screen, (255, 255, 255), (env.ball.posx, env.ball.posy), env.ball.radius)

def display(game_screen, position, text, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", 50, 50)
    text = font.render(str(text), True, color)
    game_screen.blit(text, position)

if __name__=="__main__":
    menu()