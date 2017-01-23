import pygame
import time
import random

pygame.init()

red = (200,0,0)
yellow = (200,200,0)
green = (0,200,0)
grey = (50,50,50)
black = (0,0,0)

blue = (0,100,200)

display_width = 800
display_height = 600

# player
rect_width = 40
rect_height = 40
movement_amt = -5

lights_x = 30
lights_y = 30
lights_width = 80
lights_height = 150

lights_circle_radius = 18
lights_circle_offset = lights_circle_radius*2 + lights_circle_radius/2

gameDisplay = pygame.display.set_mode((display_width,display_height))

clock = pygame.time.Clock()

t0 = time.time()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text1, text2=''):
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = text_objects(text1, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    
    gameDisplay.blit(TextSurf, TextRect)

    if text2 != '':
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects(text2, largeText)
        TextRect.center = ((display_width/2), (display_height/2+80))
        gameDisplay.blit(TextSurf, TextRect)
    
    #pygame.display.update()

    #time.sleep(2)

def display_score(score):
    score = round(score,2)
    font = pygame.font.SysFont(None, 25)
    text = font.render('Score: ' + str(score), True, blue)

    gameDisplay.blit(text, (display_width*0.85, display_width*0.05))

def won(score):
    score = str(round(score,2))
    
    gameDisplay.fill(green)
    
    message_display('You are won!', 'Score: ' + score)
    
    pygame.display.update()
    time.sleep(2.5)
    game_loop()

def caught(score):
    score = str(round(score,2))
    
    gameDisplay.fill(red)
    
    text1 = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf1, TextRect1 = text_objects('You moved on red light', text1)
    TextRect1.center = ((display_width/2), (display_height/2-180))

    text2 = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf2, TextRect2 = text_objects('and you died and lost', text2)
    TextRect2.center = ((display_width/2), (display_height/2-120))
    
    gameDisplay.blit(TextSurf1, TextRect1)
    gameDisplay.blit(TextSurf2, TextRect2)

    message_display('Score: ' + score)
    
    pygame.display.update()
    time.sleep(2.5)
    game_loop()

def get_seq(seq):
    global t0
    t1 = time.time()
    td = t1 - t0

    #print(td)

    if td >= random.uniform(2,5) and seq == 1: 
        seq = 2
        t0 = t1
        #print('SET YELLOW')
    elif td >= random.uniform(0.8,3) and seq == 2:
        seq = 3
        t0 = t1
        #print('SET RED')
    elif td >= random.uniform(2,5) and seq == 3:
        seq = 1
        t0 = t1
        #print('SET GREEN')

    return seq

def draw_lights(seq):
    pygame.draw.rect(gameDisplay, grey, (lights_x,lights_y, lights_width,lights_height))

    if seq == 1:
        pygame.draw.circle(gameDisplay, green, (int(lights_x+(lights_width/2)), \
                    int(lights_y+(lights_height/2)+lights_circle_offset)), \
                       lights_circle_radius)
    else:
        pygame.draw.circle(gameDisplay, black, (int(lights_x+(lights_width/2)), \
                    int(lights_y+(lights_height/2)+lights_circle_offset)), \
                       lights_circle_radius)

    if seq == 2:    
        pygame.draw.circle(gameDisplay, yellow, (int(lights_x+(lights_width/2)), \
                        int(lights_y+(lights_height/2))), lights_circle_radius)
    else:
        pygame.draw.circle(gameDisplay, black, (int(lights_x+(lights_width/2)), \
                        int(lights_y+(lights_height/2))), lights_circle_radius)

    if seq == 3:
        pygame.draw.circle(gameDisplay, red, (int(lights_x+(lights_width/2)), \
                        int(lights_y+(lights_height/2)-lights_circle_offset)), \
                           lights_circle_radius)
    else:
        pygame.draw.circle(gameDisplay, black, (int(lights_x+(lights_width/2)), \
                        int(lights_y+(lights_height/2)-lights_circle_offset)), \
                           lights_circle_radius)

def game_loop():
    score = 0
    seq = 1
    global t0
    t0 = time.time()

    # player
    rect_x = display_width/2 - rect_width/2
    rect_y = display_height - rect_height

    y_change = 0
    score_change = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = movement_amt
                    if seq == 1:
                        # green score
                        score_change -= 2
                    elif seq == 2:
                        # yellow score
                        score_change += -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_change = 0
                    score_change = 0

        # if red when moving you lose
        if y_change != 0 and seq == 3:
            caught(score)

        # if player reaches top
        if rect_y <= 0:
            won(score)

        rect_y += y_change
        score += score_change
            
        gameDisplay.fill((0,0,0))

        seq = get_seq(seq)

        draw_lights(seq)

        # player
        pygame.draw.rect(gameDisplay, blue, (rect_x,rect_y, rect_width,rect_height))

        display_score(score)
        
        pygame.display.update()
        clock.tick(30)

game_loop()
pygame.quit()
quit()
