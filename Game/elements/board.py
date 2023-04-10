from Game.elements.tile import Tile
from Game.elements.wall import Wall
from Game.elements.pawn import Pawn
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = []
        self.pawns = []
        tile_size = 115

        for i in range(rows):
            row = []
            for j in range(cols):
                if i == 0:
                    up = Wall(j * tile_size, i * tile_size, "horizontal", active=False)
                elif i == 1:
                    up = self.tiles[i - 1][j].wall_up
                else:
                    up = self.tiles[i - 1][j].wall_down

                if j < cols - 1:
                    right = Wall((j + 1) * tile_size, i * tile_size, "vertical")
                else:
                    right = Wall(j * tile_size + tile_size, i * tile_size, "vertical", active=False)

                if i < rows - 1:
                    down = Wall(j * tile_size, (i + 1) * tile_size, "horizontal")
                else:
                    down = Wall(j * tile_size, i * tile_size + tile_size, "horizontal", active=False)

                if j == 0:
                    left = Wall(j * tile_size, i * tile_size, "vertical", active=False)
                elif j == 1:
                    left = row[-1].wall_left
                else:
                    left = row[-1].wall_right

                tile = Tile(j * tile_size + 20, i * tile_size + 20, up, right, down, left)
                row.append(tile)

            self.tiles.append(row)



    def draw_walls(self, win):
        for row in self.tiles:
            for tile in row:
                tile.draw(win)

    def draw_pawns(self, win):
        for pawn in self.pawns:
            pawn.draw(win,110)
