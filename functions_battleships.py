import pygame
import numpy as np
import random
from classes_battleships import *
from classes_battleships import mapa
from classes_battleships import barco
from config_battleships import *

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.mixer.init()

# Set title of screen
pygame.display.set_caption("Battle Ships (Hundir Barcos)")

# Soundtracklist, loads from file directory
playlist = list()
playlist.append ( "./assets/background_music1.wav" )
playlist.append ( "./assets/background_music2.wav" )
#playlist.append ( "music1.mp3" )

# scale of images 320 x 280 aprox
hit_ship = pygame.image.load('./assets/hit_ship.jpg')
explosion_water = pygame.image.load('./assets/explosion_water.jpg')

# scale of images 800 x 400 aprox
intro_screen = pygame.image.load('./assets/battle_ship_screen.jpg')
victory_screen = pygame.image.load('./assets/victory_screen.png')
lost_battle_screen = pygame.image.load('./assets/lost_battle.jpg')


# Soundeffects / music playlist
pygame.mixer.music.load ( playlist.pop() )  # Get the first track from the playlist
pygame.mixer.music.queue ( playlist.pop() ) # Queue the 2nd song
pygame.mixer.music.set_volume(0.07)
pygame.mixer.music.set_endevent ( pygame.USEREVENT )    # Setup the end track event
pygame.mixer.music.play()           # Play the music
#pygame.mixer.Sound.set_volume(0.05)


# Initialize and calls map creation
def start_map ():
    """
    Function for starting the map creation
    Args:
    None
    Return
    grid, grid2 (objects) : Map objetct

    """
    grid = mapa().iniciar_map("AI")
    #grid = grid.create_clean_map()
    counter_ships_AI = grid[ np.where( grid == 1 )]
    print ("Ships_counter: ",len(counter_ships_AI))

    grid2 = mapa().iniciar_map("Player")

    counter_ships = grid2[ np.where( grid2 == 3 )]
    print ("Ships_counter: ",len(counter_ships))

    if len(counter_ships_AI) != len(counter_ships):
        grid, grid2 = start_map()
        return grid, grid2
    else:
        return grid, grid2
      
    


def draw_text(text,x,y,color):
      """
        Function for drawing a text on screen
        Args:
        text (str) : text string
        x (int) : x position of text
        y (int) :  y position of text
        Retunr:
        Draws text on screen
      """
      font = pygame.font.SysFont(None, 24)
      label = font.render(text, True, color)
      screen.blit(label, (x,y))


# Function for aleatory Shot from AI
def aleatory_shot (num_turno):
         """
            Function for the AI to shot on the map
            Args:
            num_turno (int) : used for setting the random seed
         """
         random.seed(num_turno)
         fila = random.randint(0, 9)
         columna = random.randint(0, 9)
         pos = fila,columna
         return pos


def turno_ai (grid2,turno,num_turno,points_ai,shots_ai,hits_ai,MARGIN2):
        """" Function for creating the AI turn strategy
        Args: 
        grid2 (object) : grid object of the player 
        turno_num (int) : turn number
        points_ai (int) : actual points of AI
        shots_ai (tuple) : shots done by ai and the positions in order to don't attack the same tile again
        hits_ai (tuple) : position as shots for marking the hits on the enemy
        
        """
        
        pygame.time.wait(100)
        shot = aleatory_shot(num_turno)
        shots_ai.append(shot)
        if shot in shots_ai:
            while shot not in shots_ai and shot not in hits_ai:
                shot = aleatory_shot(num_turno)


        #print(shot[0][1])
        print ("AI")
        print(type(shot))
        print(shot)
        pygame.time.wait(400)
        if grid2[shot[0]][shot[1]] == 3:
            grid2[shot[0]][shot[1]] = 2
            hits_ai.append(shot)
            points_ai = points_ai+1    
            soundeffect = pygame.mixer.Sound("./assets/explosion.wav")
            pygame.mixer.Sound.play(soundeffect)
            turno = "AI"
            num_turno = num_turno+1
            screen.blit(hit_ship, (MARGIN2, 400))
            pygame.display.update()
            pygame.time.wait(500)
            
        elif grid2[shot[0]][shot[1]] != 3 and grid2[shot[0]][shot[1]] != 4 and  grid2[shot[0]][shot[1]] != 2:
                    grid2[shot[0]][shot[1]] = 4
                    turno = "player"
                    num_turno = num_turno+1
                    soundeffect = pygame.mixer.Sound("./assets/shoot_ai.wav")
                    pygame.mixer.Sound.play(soundeffect)
                    screen.blit(explosion_water, (MARGIN2, 400))
                    pygame.display.update()
                    pygame.time.wait(500)

        return turno, num_turno, points_ai, shots_ai, hits_ai



def battelfield_update(grid, grid2, MARGIN, MARGIN2, WIDTH, HEIGHT, offset_x,offset_y,screen, NAVY, GREEN,RED,BLUE,GREY,CHARCOL):
    
    """" Battlefield update function, used to update the grid
    
    Args:
    grid (object) : map of AI
    grid2 (object) : Map of player 2
    Margin (int)  : distance from left in pixels
    Margin2 (int) : Distance from left in pixels
    Width (int) : Width of screen
    Height (int) : Heigth of screen
    offset_x (int) : additional margin of x
    offset_y (int) : additional margin of y
    screen (object)  : screen object
    NAVY, GREEN, RED .. (tuple) : Colorcode RGB
    

    Return:
    Updates the map
    
    """



    screen.fill(NAVY) # ScreenBackground
    draw_text("Enemy ships", offset_x+80,40, "RED")
    draw_text("Your ships", MARGIN2+offset_x+30,40, "GREEN")
    
 
    ## VISUALIZATION OF AI SHIPS /  TILES  
    for row in range(10):
        for column in range(10):
            color = BLUE


            # UNCOMMMENT THIS FOR REVEAL THE AI SHIPS ON MAP
            # if grid[row][column] == 1:   
            #      color = RED
            #      pygame.draw.rect(screen,
            #                  color,
            #                  [(MARGIN + WIDTH) * column + MARGIN+offset_x,
            #                   (MARGIN + HEIGHT) * row + MARGIN+offset_y,
            #                   WIDTH,
            #                  HEIGHT])


            if grid[row][column] == 2:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN+offset_x,
                              (MARGIN + HEIGHT) * row + MARGIN+offset_y,
                              WIDTH,
                              HEIGHT])

            
            if grid[row][column] == 4:
                color = GREY
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN+offset_x,
                              (MARGIN + HEIGHT) * row + MARGIN+offset_y,
                              WIDTH,
                              HEIGHT])

    ### END OF TILE COLOR CHANGINGS AI
    

    ## VISUALIZATION OF PLAYER SHIPS /  TILES         
    
    for rowx in range(10):
        for columnx in range(10):
            colorx = BLUE

            if grid2[rowx][columnx] == 3:
                colorx = GREEN
            pygame.draw.rect(screen,
                             colorx,
                             [(MARGIN + WIDTH) * columnx + MARGIN2,
                              (MARGIN + HEIGHT) * rowx + MARGIN+offset_y,
                              WIDTH,
                              HEIGHT])


            if grid2[rowx][columnx] == 2:
                colorx = CHARCOL
            pygame.draw.rect(screen,
                             colorx,
                             [(MARGIN + WIDTH) * columnx + MARGIN2,
                              (MARGIN + HEIGHT) * rowx + MARGIN+offset_y,
                              WIDTH,
                              HEIGHT])
            
                
            if grid2[rowx][columnx] == 4:
                colorx = GREY
            pygame.draw.rect(screen,
                             colorx,
                             [(MARGIN + WIDTH) * columnx + MARGIN2,
                              (MARGIN + HEIGHT) * rowx + MARGIN+offset_y,
                              WIDTH,
                              HEIGHT])



    ### END OF TILE COLOR CHANGINGS Player


def checkhits(clicks,hit_ship,done,grid,grid2,WIDTH,HEIGHT,MARGIN,MARGIN2,offset_y,offset_x,turno,points_player,num_turno,screen,playlist):
        """
        Function checkhits monitors the clicks and events in the map, also the player shots
        Args:
        click (list) : use last click
        grid (array) : map object
        grid2 (array) : map object
        WIDTH (int): screen width
        HEIGHT (int): screem height
        MARGIN (int) : distance from left
        MARGIN2 (int) : distance from left
        offset_y (int) : additional distance
        offset_x (int) : additional distance
        turno (str) : indicates the turn owner
        points_player : number of player points
        num_turno (int) : indicates the turn number
        screen (object) : PyGame Screen object
        playlist (list) : list of background music

        Return:
        row and column clicked, if a ai ship is hit
        
        """


           ## RECEIVE and handle INPUT EVENTS FROM USER
        try:
            


            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                   
                    done = True  # Flag that we are done so we exit this loop
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = (pos[0]-offset_y) // (WIDTH + (MARGIN))
                    row = (pos[1]-offset_x) // (HEIGHT + (MARGIN))
                    column = column
                    row = row

                    # Set that location in grid of AI to tile type 1
                    if grid[row][column] == 1 and grid[row][column] != 4:

                        grid[row][column] = 2
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        clicks.append([row,column]) # Write clicks to list

                        
                    
                        
                        soundeffect = pygame.mixer.Sound("./assets/explosion.wav")
                        pygame.mixer.Sound.play(soundeffect)
                        turno = "player"
                        points_player = points_player+1
                        num_turno = num_turno+1
                        screen.blit(hit_ship, (offset_x, 400))
                        pygame.display.update()
                        
                        pygame.time.wait(500)
                    
                    elif grid[row][column] != 1 and grid[row][column] != 4 and grid[row][column] != 2:
                            grid[row][column] = 4
                            print("Click ", pos, "Grid coordinates: ", row, column)
                            clicks.append([row,column]) # Write clicks to list
                            
                            
                            
                            soundeffect= pygame.mixer.Sound("./assets/shoot_aside.wav")
                            pygame.mixer.Sound.play(soundeffect)
                            turno = "AI"
                            num_turno = num_turno+1
                            screen.blit(explosion_water, (offset_x, 400))
                            pygame.display.update()
                            pygame.time.wait(500)
                
            
                
                    if event.type == pygame.USEREVENT:    # A track has ended
                            if len ( playlist ) > 0:       # If there are more tracks in the queue...
                                pygame.mixer.music.queue ( playlist.pop() ) # Q  
            
            
            
            
            return num_turno,turno,points_player,clicks,done
                    
                    
                
                        

                
        except:
                print("error")
                draw_text("You can only click \n in the fields", offset_x,550, "RED")
                
                #pygame.display.flip()
                pygame.time.wait(500)
                
    
    

def game_turns (clicks,grid,grid2,screen,done,gamefinal,points_player,points_ai,MARGIN,MARGIN2,offset_x,texto_turn_ai,turno,num_turno,hits_ai,shots_ai,max_points,winnermessage_player,texto_turn_player,winnermessage_ai,NAVY,RED,victory_screen,lost_battle_screen):
    """ Function for the turn logic and point control
    
    Args:
    clicks,grid,grid2,screen,done,gamefinal,points_player,points_ai,MARGIN,MARGIN2,offset_x,texto_turn_ai,turno,num_turno,hits_ai,shots_ai,max_points,winnermessage_player,texto_turn_player,winnermessage_ai,NAVY,RED,victory_screen,lost_battle_screen

    Return:
    turno, num_turno, points_ai, shots_ai, hits_ai, gamefinal, points_ai, points_player,done
    
    """


    ## If there is any click show statistics and go ahaed to turns
    if len(clicks) >0:
       # print(len(clicks))
        texto_puntos_AI = " Points enemy: " + str(points_ai)
        texto_puntos_player = " Your points: " + str(points_player)
     #   texto = "Grid coordinates: "+str(clicks[-1:])
        draw_text(texto_puntos_player,  MARGIN2+offset_x+30,360, "Green")
        draw_text(texto_puntos_AI, offset_x+80,360, "RED")
      #  font = pygame.font.SysFont(None, 24)
      #  img = font.render(texto, True, RED)
       # texti = screen.blit(img, (offset_x, 580))


    # Turn of AI 
    if turno == "AI":
            font = pygame.font.SysFont(None, 56)
            pygame.time.wait(100)
            draw_text(texto_turn_ai, MARGIN2+80,15, "WHITE")
            turno, num_turno, points_ai, shots_ai, hits_ai = turno_ai(grid2,turno,num_turno,points_ai,shots_ai,hits_ai,MARGIN2)
            #b1 = button(screen, (340, 550), "Restart")
  

    # Turn of Player
    if turno == "player":
            font = pygame.font.SysFont(None, 56)
            draw_text(texto_turn_player, offset_x+80,15, "WHITE")
            pygame.time.wait(100)        
            
           
    if points_player >= max_points:

        screen.fill(NAVY)
        #if gamefinal == False:
            #start_ticks=pygame.time.get_ticks() #starter tick
        font = pygame.font.SysFont(None, 220)
        draw_text(winnermessage_player, 300,30, "WHITE") 
        screen.blit(victory_screen, (1, 100))
       # pygame.time.wait(1000)
        
       #seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        #draw_text("The game restarts in.."+str(int(seconds)), 300,60, "WHITE")  
        #pygame.display.update() 
        pygame.time.wait(3000)
        #if seconds>10: # if more than 10 seconds close the game
               #pygame.quit() # Change to restart

        #b1 = button(screen, (offset_x+200, 500), "Restart") 
        
        
        #done = True
        gamefinal = True
        #pygame.display.update
        #pygame.time.wait(1000)
      
        
        #restart game
        #pygame.quit()
        
    
    elif points_ai >= max_points:
        screen.fill(NAVY)
        if gamefinal == False:
            start_ticks=pygame.time.get_ticks() #starter tick
        font = pygame.font.SysFont(None, 220)
        draw_text(winnermessage_ai, 300,30, "WHITE") 
        screen.blit(lost_battle_screen, (1, 100))
        # pygame.time.wait(1000)

        # seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        # draw_text("The game restarts in.."+str(int(seconds)), 300,60, "WHITE")  
        # pygame.display.update
        pygame.time.wait(4000)
       # if seconds>10: # if more than 10 seconds close the game
                #pygame.quit() # Change to restart

        #b1 = button(screen, (offset_x+200, 500), "Restart") 
        gamefinal = True
        # done = True
        # pygame.display.update
        # pygame.time.wait(1000)
       
    return turno, num_turno, points_ai, shots_ai, hits_ai, gamefinal, points_ai, points_player,done



def initscreen (startgame,screen,welcome_text,NAVY):
        """
        Function for displaying the initial loading screen
        """
        if startgame == True:
            screen.fill(NAVY)
            screen.blit(intro_screen, (1, 100))
            #font = pygame.font.SysFont(None, 40)
            draw_text(welcome_text, 300,50, "WHITE")      
            draw_text("..the game is starting..", 300,520, "WHITE")
            pygame.display.flip() 
            pygame.time.wait(3000)
            startgame = False
            return startgame