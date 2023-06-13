# tile.py
from Game.elements.wall import Wall
import pygame

class Tile:
    def __init__(self, x, y,size,index, wall_up, wall_right, wall_down, wall_left):
        self.x = x
        self.y = y
        self.x_index = index[0]
        self.y_index = index[1]

        self.size = size - 20

        # instance of walls
        self.wall_up = wall_up
        self.wall_right = wall_right
        self.wall_down = wall_down
        self.wall_left = wall_left
        
        self.pawn = None
        self.color = (200, 200, 200)

    def draw(self, win):
        # Draw the tile itself as a rectangle
        self.rect = pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        self.win = win
        self.draw_walls(win, [True, True, True, True])

    def draw_walls(self, win, walls_to_show):
        walls = self.GetWalls()
        for i in range(len(walls_to_show)):
            if walls_to_show[i] and walls[i] is not None:
                walls[i].draw(win)

    def hover(self):
        pygame.draw.rect(self.win, (160, 160, 160), self.rect)
    
    def get_rect(self):
        return self.rect

    def GetWalls(self):
        return [self.wall_up, self.wall_right, self.wall_down, self.wall_left]
