import pygame
import time
import random

pygame.init()

disp_width = 800
disp_hght = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

car_image = pygame.image.load('racecar.png')
car_width = 73

gameDisplay = pygame.display.set_mode((disp_width, disp_hght))

def car(x, y):
    gameDisplay.blit(car_image, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, large_text)
    TextRect.center= ((disp_width / 2), (disp_hght / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('Crashed')

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

pygame.display.set_caption('A race game')
clock = pygame.time.Clock()

def game_loop():
    x = (disp_width * 0.45)
    y = (disp_hght * 0.8)
    x_change = 0
    car_speed = 0
    gameExit = False

    # Random thing generation
    thing_startx = random.randrange(0,disp_width)
    thing_starty = -600
    thing_speed = 7

    thing_width = 25
    thing_height = 25

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_change = 0

            x += x_change
            gameDisplay.fill(white)
            things(thing_startx, thing_starty, thing_width, thing_height, black)
            thing_starty += thing_speed
            car(x, y)

            if x > disp_width - car_width:
                x = disp_width - car_width
                crash()
            if x < 0:
                x = 0
                crash()

            if thing_starty > disp_hght:
                thing_starty = 0 - thing_height
                thing_startx = random.randrange(0,disp_width)

            if y < thing_starty+thing_height:
                print('y crossover')
                if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                    print('x crossover')
                    crash()

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
