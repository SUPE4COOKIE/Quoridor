from pygame.draw import circle

class Pawn:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface, tile_size):
        pawn_radius = tile_size // 4
        pawn_x = self.x * tile_size + tile_size // 2
        pawn_y = self.y * tile_size + tile_size // 2
        print(pawn_x, pawn_y)
        circle(surface, self.color, (pawn_x, pawn_y), pawn_radius)

