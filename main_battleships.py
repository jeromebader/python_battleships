"""
HUNDIR FLOTAS
BATTLE SHIP 
PyGame
Christian J. Bader


"""

# Import game Libs
import pygame
import numpy as np

from config_battleships import *
from classes_battleships import *
from functions_battleships import *
 
# Initialize pygame
pygame.init()
 
def main ():

    
    
# Loop until the user clicks the close button.
    done = False

    # Setting of start variables
    # Game variables
    points_player = 0
    points_ai = 0
    turno = "player"
    num_turno = 0
    shots_ai = []
    hits_ai = []
    startgame = True
    gamefinal = False
    clicked_restart = False
    clicks = []
    
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # We requiere 2 maps, one for the AI and the other for representing the map with player ships
    grid, grid2 = start_map()
    max_points = len(grid[ np.where( grid == 1 )])

    # Limit to 80 frames per second
    clock.tick(80)


    # -------- Main Program Loop -----------
    while not done:

        #pygame.event.pump()

        # Show Intro Screen
        startgame = initscreen (startgame,screen,welcome_text,NAVY)

        
        # check the position of mouse and click with the battlefield and update variables
        num_turno,turno,points_player,clicks,done = checkhits(clicks,hit_ship,done,grid,grid2,WIDTH,HEIGHT,MARGIN,MARGIN2,offset_y,offset_x,turno,points_player,num_turno,screen,playlist)
        
        # Update Grid with shots and hits
        battelfield_update(grid, grid2, MARGIN, MARGIN2, WIDTH, HEIGHT, offset_x,offset_y,screen,NAVY, GREEN,RED,BLUE,GREY,CHARCOL)


        # Go ahead and update game points and turns   
        turno, num_turno, points_ai, shots_ai, hits_ai, gamefinal, points_ai, points_player, done = game_turns (clicks,grid,grid2,screen,done,gamefinal,points_player,points_ai,MARGIN,MARGIN2,offset_x,texto_turn_ai,turno,num_turno,hits_ai,shots_ai,max_points,winnermessage_player,texto_turn_player,winnermessage_ai,NAVY,RED,victory_screen, lost_battle_screen)
    
        
        
        # Restart Button
        # RE-ENGENEERING necessary

        # Screen update / flipping
        pygame.display.flip()   


    # OUT OF LOOP   
    # without quite line, the program will 'hang'
    
    pygame.quit()

    

main()  # Call Main
pygame.quit()