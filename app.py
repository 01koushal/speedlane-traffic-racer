import pygame
import random
import math
from pygame import mixer
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Traffic Racer")

icon = pygame.image.load('race (2).png')
pygame.display.set_icon(icon)

background=pygame.image.load('road1.png')
background_y=0

score_value=0
font=pygame.font.Font('freesansbold.ttf',24)
textx=10
texty=10
highscore_value=0

big_font=pygame.font.Font('freesansbold.ttf',48)


player_img = pygame.image.load('redsports.png')
player_x = 370
player_y = 480
player_xchange=0
player_ychange=0




traffic_img=[]
traffic_x =[]
traffic_y =[]
traffic_xchange=[]
traffic_ychange=[]
traffic_num=8
trafficxchoice=[10,110,210,320,420,530,630,730]
trafficychoice=[0,110,210,320,420,530]
a=["red.png","ash.png","yellow.png","green.png","orange.png","blue.png"]

for i in range(traffic_num):
    traffic_img.append(pygame.image.load(random.choice(a)))
    traffic_x.append(random.choice(trafficxchoice))
    traffic_y.append(random.choice(trafficychoice))
    traffic_xchange.append(0)
    traffic_ychange.append(0)

#music
bg_music = 'sample.wav'
gameover_music = 'Game Over.wav'

def reset_game():
    global player_x, player_y, player_xchange, player_ychange
    global traffic_x, traffic_y, traffic_ychange
    global score_value, background_y

    # Reset player
    player_x = 370
    player_y = 480
    player_xchange = 0
    player_ychange = 0

    # Reset score and background
    score_value = 0
    background_y = 0

    # Reset traffic positions
    for i in range(traffic_num):
        traffic_x[i] = random.choice(trafficxchoice)
        traffic_y[i] = random.choice(trafficychoice) 
        traffic_ychange[i] = 0

def draw_player(x,y):
    screen.blit(player_img,(x,y))
    
    

def draw_traffic(x,y,i):
    screen.blit(traffic_img[i],(x,y))
    

def show_score(x,y):
    score=font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def show_highscore(x,y):
    high_score=font.render("High Score:"+str(highscore_value),True,(255,255,255))
    screen.blit(high_score,(x,y))
    

def show_gameover(x,y):
    text_gameover=big_font.render("Game Over",True,(255,255,255))
    screen.blit(text_gameover,(x,y-30))
    text_enter=font.render("Press Enter to Start",True,(255,255,255))
    screen.blit(text_enter,(x+10,y+30))
    show_score(x+50,y+80)
    show_highscore(x+50,y+100)


clock = pygame.time.Clock()
game_state="start"
running=True
mixer.music.load(bg_music)
mixer.music.play(-1)
while running:
    screen.fill((0, 0, 0)) 
    clock.tick(60)
    
    events = pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            running=False
    if game_state=="start":
        screen.blit(background,(0,0))
        text_enter=font.render("Press Enter to Start",True,(255,255,255))
        screen.blit(text_enter,(300+10,300+60))
        mixer.music.load(bg_music)
        mixer.music.play(-1)
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    game_state="running"

    if game_state=="pause":
        screen.blit(background,(0,0))
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    game_state="running"
    if game_state=="game_over":
        screen.fill((0,0,0))
        show_gameover(280,300)
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    reset_game()
                    reset_game()
                    mixer.music.stop()
                    mixer.music.load(gameover_music)
                    mixer.music.play(-1)  # resume background loop
                    game_state="start"



    if game_state=="running":
        screen.blit(background,(0,0))
        speed = score_value // 20 + 4


        background_y +=10+speed  # Adjust speed as needed
        if background_y >= 600:
            background_y = 0

        # Draw the background twice for seamless scrolling
        screen.blit(background, (0, background_y))
        screen.blit(background, (0, background_y - 600))
        
        draw_player(player_x,player_y)
        for i in range(traffic_num):
            draw_traffic(traffic_x[i],traffic_y[i],i)
        for event in events:
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    player_xchange-=5
                if event.key==pygame.K_RIGHT:
                    player_xchange+=5
                if event.key==pygame.K_p:
                    game_state="pause"
                

            if event.type==pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_xchange = 0
        player_x=player_xchange+player_x
        if  player_x<=0:
            player_x=0
        elif player_x>=740:
            player_x=740
            
        for i in range(traffic_num):
            traffic_ychange[i]+=1
            traffic_y[i]+=traffic_ychange[i]+speed
            if traffic_y[i]>=0:
                traffic_ychange[i]=1
            elif traffic_y[i]<=350:
                traffic_ychange[i]=1
            if traffic_y[i] > 600:
                score_value += 1
                if(score_value>highscore_value):
                    highscore_value=score_value

                valid_spawn = False
                while not valid_spawn:
                    new_x = random.choice(trafficxchoice)
                    new_y = random.choice(trafficychoice) - 600

                    valid_spawn = True
                    for j in range(traffic_num):
                        if i != j:
                            # Check distance between new spawn and other cars
                            dist = math.sqrt((new_x - traffic_x[j])**2 + (new_y - traffic_y[j])**2)
                            if dist < 100:  # adjust spacing threshold
                                valid_spawn = False
                                break
                
                traffic_x[i] = new_x
                traffic_y[i] = new_y
                # --- Show score ---
        show_score(textx, texty)
        show_highscore(textx,texty+20)

        # --- Collision detection with rects ---
        # Update player rect
        player_rect = player_img.get_rect()
        player_rect.topleft = (player_x, player_y)

        for i in range(traffic_num):
            # Update traffic rect
            traffic_rect = traffic_img[i].get_rect()
            traffic_rect.topleft = (traffic_x[i], traffic_y[i])

            # Collision check
            if player_rect.colliderect(traffic_rect):
                game_state = "game_over"
                mixer.music.stop()                      # stop background
                mixer.music.load(gameover_music)        # load game over
                mixer.music.play() 
                break


        
        
        draw_traffic(traffic_x[i],traffic_y[i],i)
            

            
            

    pygame.display.update()
    
