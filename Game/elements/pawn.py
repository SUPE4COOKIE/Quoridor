from pygame.draw import circle

class Pawn:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.pawn = None

    def draw_on_tile(self, surface, tile):

        self.surface = surface
        self.pawn = circle(surface, self.color, (tile.x + tile.size //2 , tile.y + tile.size //2) , tile.size // 4)

    def move(self, tile):
        self.x = tile.x_index
        self.y = tile.y_index
    
    def get_position(self):
        return (self.x, self.y)

    def get_circle(self):
        return self.pawn