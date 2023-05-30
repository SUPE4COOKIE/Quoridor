from pygame.draw import circle

class Pawn:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.pawn = None

    def draw_on_tile(self, surface, tile):
        self.pawn = circle(surface, self.color, (tile.x + tile.size //2 , tile.y + tile.size //2) , tile.size // 4)

    def remove_from_tile(self, surface, tile):
        if self.pawn is not None:
            self.pawn.fill(tile.color)

    def get_circle(self):
        return self.pawn