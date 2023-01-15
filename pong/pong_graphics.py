import pong
import pygame
import time

def network_vs_player():
    env = pong.Env()
    fps = 60
    pygame.init()
    game_screen = pygame.display.set_mode(env.screen)
    pygame.display.set_caption('pong')
    env.new_game()
    running = True
    while env.paddle1.score < 1 and env.paddle2.score < 1 and running:
        frame_time = time.time()
        draw(env, game_screen)
        env.update_env()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            env.paddle2.action(2)
        if keys[pygame.K_UP]:
            env.paddle2.action(0)
        if 1/fps - time.time() + frame_time > 0.001:
            time.sleep(1/fps - time.time() + frame_time)
    if env.paddle1.score == 10:
        winning_screen(game_screen, 0)
        pygame.display.flip()
        time.sleep(3)
        return 0
    winning_screen(game_screen, 2)
    pygame.display.flip()
    time.sleep(3)
    return 2

def winning_screen(game_screen, winner):
    if winner == 0:
        display(game_screen, (300, 200), "ai won!")
    if winner == 2:
        display(game_screen, (300, 250), "player won!")

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
    network_vs_player()