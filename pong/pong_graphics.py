import pong
import pygame
import time


def game(game_screen, game_type=1):
    # the function gets a game screen from pygame and game type.
    # the function uses the env object to create a game and present it on the game screen
    # 1. network vs player, 2. player vs player, 3. network vs network
    env = pong.Env()  # create a new environment
    fps = 60  # set the fps for the game
    env.new_game()  # start a new game
    running = True
    draw(env, game_screen)
    # game stops when a player get to 10 points or when the you leave the game
    while env.paddle1.score < 10 and env.paddle2.score < 10 and running:
        frame_time = time.time()  # messure time to keep a stable frame rate
        draw(env, game_screen)  # draw the frame
        env.update_env(game_type)  # update the backend of the game
        for event in pygame.event.get():  # exit the loop if the player closed the game screen
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()  # get input for actions and leaving the game
        if keys[pygame.K_ESCAPE]:
            running = False
        if game_type != 3:  # input for right paddle
            if keys[pygame.K_DOWN]:
                env.paddle2.action(2)
            if keys[pygame.K_UP]:
                env.paddle2.action(0)
        if game_type == 2:  # input for left paddle
            if keys[pygame.K_s]:
                env.paddle1.action(2)
            if keys[pygame.K_w]:
                env.paddle1.action(0)
        if 1/fps - time.time() + frame_time > 0.001:  # wait the remaining time to keep a stable frame rate
            time.sleep(1/fps - time.time() + frame_time)
    if env.paddle1.score == 10:  # check who won the game
        draw(env, game_screen)  # draw the final frame
        winning_screen(game_screen, env, game_type)  # draw the winning screen
    else:
        draw(env, game_screen)  # draw the final frame
        winning_screen(game_screen, env, game_type)  # draw the winning screen


def restart_button(game_screen, game_type):
    # the function gets a game screen from pygame and a game type
    # the function draws a restart button and a menu button on the screen
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(150, 400, 200, 100))  # draw the restart button
    display(game_screen, (170, 415), "restart",
            color=(0, 255, 0))  # draw the restart text
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(450, 400, 200, 100))  # draw the menu button
    display(game_screen, (490, 415), "menu",
            color=(0, 255, 0))  # draw the menu text
    pygame.display.flip()  # present the buttons
    running = True
    time.sleep(0.2)
    while running:  # keeps the window open until the player close it or ends the function
        for event in pygame.event.get():  # if the player leaves the game screen or press espace the screen closes
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # if the player pressed the mouse, get the mouse position
                mouse = pygame.mouse.get_pos()
                # check if the player pressed on the restart button
                if mouse[0] > 150 and mouse[0] < 350 and mouse[1] > 400 and mouse[1] < 500:
                    game(game_screen, game_type)  # starts a new game
                    running = False  # closes the function when the game ends
                # check if the player pressed on the menu button
                if mouse[0] > 450 and mouse[0] < 650 and mouse[1] > 400 and mouse[1] < 500:
                    menu()  # shows the menu
                    running = False  # closes the function when the menu closes


def menu():
    # the function restarts the screen and present the menu on it
    pygame.init()  # restart the screen to the menu
    game_screen = pygame.display.set_mode((800, 600))
    display(game_screen, (330, 0), "menu:",
            color=(0, 255, 0))  # draw the menu text
    pygame.display.set_caption('pong')  # set the screen title to pong
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(200, 70, 400, 100))  # the player vs player button
    display(game_screen, (210, 85), "player vs player",
            color=(0, 255, 0))  # the player vs player text
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(200, 200, 400, 100))  # the ai vs player button
    display(game_screen, (210, 215), "ai vs player",
            color=(0, 255, 0))  # the ai vs player text
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(200, 330, 400, 100))  # the ai vs ai button
    display(game_screen, (210, 345), "ai vs ai",
            color=(0, 255, 0))  # the ai vs ai text
    pygame.draw.rect(game_screen, (150, 150, 150),
                     pygame.Rect(200, 460, 400, 100))  # the ai vs ai button
    display(game_screen, (210, 475), "instructions",
            color=(0, 255, 0))  # the ai vs ai text
    pygame.display.flip()  # display the frame
    time.sleep(0.2)
    running = True
    while running:  # keeps the window open until the player close it or ends the function
        for event in pygame.event.get():  # if the player leaves the game screen or press espace the screen closes
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # if the player pressed the mouse, get the mouse position
                mouse = pygame.mouse.get_pos()
                # check if the player pressed on the player vs player button
                if 200 < mouse[0] < 600 and 70 < mouse[1] < 170:
                    game(game_screen, 2)  # starts a new player vs player game
                    running = False  # closes the function when the game ends
                # check if the player pressed on the ai vs player button
                elif 200 < mouse[0] < 600 and 200 < mouse[1] < 300:
                    game(game_screen, 1)  # starts a new ai vs player game
                    running = False  # closes the function when the game ends
                # check if the player pressed on the ai vs ai button
                elif 200 < mouse[0] < 600 and 330 < mouse[1] < 430:
                    game(game_screen, 3)  # starts a new ai vs ai game
                    running = False  # closes the function when the game ends
                # check if the player pressed on the instructions button
                elif 200 < mouse[0] < 600 and 460 < mouse[1] < 560:
                    # display the instructions screen
                    instructions(game_screen)
                    running = False  # closes the function when the screen is closed


def winning_screen(game_screen, env, game_type):
    # the function gets a game screen from pygame, the env object and the game type
    # the function present who won and then activate the restart button function
    if env.paddle1.score > env.paddle2.score:  # check who won and display the text
        display(game_screen, (220, 250), "left paddle won!")
    elif env.paddle1.score < env.paddle2.score:
        display(game_screen, (200, 250), "right paddle won!")
    else:
        display(game_screen, (300, 250), "Its a tie!")
    # activate the restart button function to start a new game or go to the menu
    restart_button(game_screen, game_type)
    pygame.display.flip()  # present the winning screen


def draw(env, game_screen):
    # the function gets an env object and the game screen from pygame
    # the function draws the frame on the game screen and presents it
    game_screen.fill((0, 0, 0))  # fill the screen with black background
    pygame.draw.line(game_screen, (100, 100, 100),
                     (env.screen[0] // 2, 0), (env.screen[0] // 2, env.screen[1]), 2)  # draw the middle line
    # draw the score of the paddles
    display(game_screen, (310, 20), env.paddle1.score)
    display(game_screen, (460, 20), env.paddle2.score)
    # draw the paddldes
    pygame.draw.rect(game_screen, (255, 255, 255), env.paddle1.rect)
    pygame.draw.rect(game_screen, (255, 255, 255), env.paddle2.rect)
    pygame.draw.circle(game_screen, (255, 255, 255),
                       (env.ball.posx, env.ball.posy), env.ball.radius)  # draw the ball
    pygame.display.flip()  # present the frame


def display(game_screen, position, text, color=(255, 255, 255), size=50):
    # the function gets a game screen from pygame, position and text
    # the function draws the text on the game screen
    # select the font of the text
    font = pygame.font.SysFont("Arial", size, 50)
    text = font.render(str(text), True, color)  # render the text
    game_screen.blit(text, position)  # present the text


def instructions(game_screen):
    # the function gets a game screen from pygame
    # the function displays instructions on the screen and waits for the user to return to the menu
    game_screen.fill((0, 0, 0))  # fill the screen with black background
    display(game_screen, (230, 0), "Instructions:", color=(
        0, 255, 0))  # draw the instructions title
    # draw the instructions
    display(game_screen, (0, 100),
            "- Use the arrow keys or 'w' and 's' keys to move your paddle", size=25)
    display(game_screen, (0, 150),
            "- Try to bounce the ball past your opponent's paddle to score points", size=25)
    display(game_screen, (0, 200),
            "- The first player to reach 10 points wins the game", size=25)
    display(game_screen, (0, 250),
            "- Press 'Esc' to exit the game at any time", size=25)
    display(game_screen, (0, 300),
            "- When playing against AI, use the arrow keys only", size=25)
    pygame.draw.rect(game_screen, (150, 150, 150), pygame.Rect(
        300, 400, 200, 100))  # the menu button
    display(game_screen, (340, 415), "menu",
            color=(0, 255, 0))  # the menu text
    pygame.display.flip()  # display the frame
    time.sleep(0.2)
    running = True
    # leaving the screen results in coming back to the menu
    while running:  # stay in instruction until leaving back to menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # check if we pressed x
                menu()  # come back to menu
                running = False  # closes the function when the menu closes
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:  # check if we pressed escape
                menu()  # come back to menu
                running = False  # closes the function when the menu closes
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # check if we pressed the menu button
                if mouse[0] > 300 and mouse[0] < 500 and mouse[1] > 400 and mouse[1] < 500:
                    menu()  # come back to menu
                    running = False  # closes the function when the menu closes


if __name__ == "__main__":
    menu()
