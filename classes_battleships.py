import pygame
import numpy as np
import random


class mapa:
    """ Class for creating the maps and set the ships"""
 
    grid_sizex = 10  # constants because the map x is 10 fields
    grid_sizey = 10 # constants because the map y is 10 fields


    def __init__ (self):
        
        self.size_mapx = mapa.grid_sizex
        self.size_mapy = mapa.grid_sizey
        
       
       
    
    # Create a 2 dimensional array.
    def create_clean_map (self):
            grid = []
            for row in range(self.size_mapx):
                # Add an empty array that will hold each cell
               
                grid.append([])
                for column in range(self.size_mapy):
                    grid[row].append(0)  # Append a cell
                    

            grid = np.array(grid) # converts list in numpy array
            return grid


    def place_ships (self,grid,nave, player,length):
            contador_ai = 0
            contador_player = 0
            for j in range(len(nave)):
                
                    print(nave[j])
                    print(nave[j][0])
                    print(nave[j][1])
                    if player == "Player":
                        if grid[nave[j][0],nave[j][1]] !=3:  # Player ships
                            grid[nave[j][0],nave[j][1]] = 3 # Player ships
                            contador_player =+ 1
                        
                       
                    elif player == "AI":
                        if grid[nave[j][0],nave[j][1]] !=1: # AI ships
                            grid[nave[j][0],nave[j][1]] = 1  # AI ships
                            contador_ai =+ 1
                    else:
                        #nave = barco(player,length,10).create_ship_random(length)  # If in position exists ship, try a new creation
                        return self.iniciar_map(player)
                    
                    #print ("Contador     ",contador_player,contador_ai)
                    #return contador_player,contador_ai

        #  if player == "AI":
        #         for k in range(len(nave)):
                
        #             print(nave[k])
        #             print(nave[k][0])
        #             print(nave[k][1])
        #             if grid[nave[k][0],nave[k][1]] !=1: # AI ships
        #                  grid[nave[k][0],nave[k][1]] = 1  # AI ships
        #                #  return True
        #             else:
        #                # nave = barco(player,length,10).create_ship_random(length)  # If in position exists ship, try a new creation
        #                 return self.iniciar_map(player)
         





    def iniciar_map (self,player):
        """
        Class for initialize the map using a clean map and then placing the ships on it
        Arg:
        player (str) : indicates the player


        """


        try:
           contador_barcos = 0
           lista_barcos = [1,1,2,2,3,4]  # Constants of ships or ship-length for placing into the map
           grid = self.create_clean_map()

           ## CREATE SHIPS
           
           for i in lista_barcos:
                print(i)
                nave = barco(player,i,10).create_ship_random(i)
                
                self.place_ships(grid,nave,player,i)
                contador_barcos = contador_barcos+1
                print (f"nave {i} del player {player} es:",nave)

           print("nave final",contador_barcos)
           if contador_barcos != len (lista_barcos):
                return self.iniciar_map(player)

           print(player) 

           print ("----")
     
        
           return grid
           
        




        except:
            print ("error initialize map")
            self.iniciar_map(player)
            pass

    
    
 

class barco:
    """ Class for Ships creation"""

    def __init__ (self,mapid,length,gridsize=10):
           self.mapid = mapid
           self.gridsize = gridsize
           self.length = length
           
          

    def try_place_ship(self,row, col, direction, length):
                """Based on direction will call helper method to try and place a ship on the grid"""
                grid_size = self.gridsize

                start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
                if direction == "East":
                    if col - length < 0:
                        return False
                    start_col = col - length + 1

                elif direction == "West":
                    if col + length >= grid_size:
                        return False
                    end_col = col + length

                elif direction == "North":
                    if row - length < 0:
                        return False
                    start_row = row - length + 1

                elif direction == "South":
                    if row + length >= grid_size:
                        return False
                    end_row = row + length

                #print(start_row, end_row, start_col, end_col)
                
                return ((start_row, end_row), (start_col, end_col))

    def create_ship_random (self,length):
        
         fila = random.randint(1, 9)
         places = []
         columna = random.randint(1, 9)
         opciones = ["East", "West", "North","South"]
         orientation = random.choice(opciones)
         positioning = self.try_place_ship(fila,columna,orientation,length )
         print(f"positioning{positioning}")
         if positioning == False:
            return self.create_ship_random(length)
         else:
            posiciones = self.try_place_ship(fila,columna,orientation,length )
            if not posiciones[0]:
                print ("Attention")
            # Check if ther is already a ship?
             

            for i in range(posiciones[0][0],posiciones[0][1]):
                for j in range(posiciones[1][0],posiciones[1][1]):
                    pos = j,i
                    print ("pos",pos)
                    if pos in places:
                       return self.create_ship_random(length)
                    else:
                      places.append(pos)

         #print(places)
         return places
