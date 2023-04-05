from Game.elements.tile import Tile
from Game.elements.wall import Wall
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = []

        for i in range(rows):
            row = []
            for j in range(cols):
                up = Wall(j * 100, i * 100, "horizontal") if i == 0 else self.tiles[-1][j].wall_down
                right = Wall((j + 1) * 100 - 10, i * 100, "vertical")
                down = Wall(j * 100, (i + 1) * 100 - 10, "horizontal")
                left = self.tiles[-1][j].wall_right if i > 0 else Wall(j * 100, i * 100, "vertical")

                tile = Tile(j * 100 , i * 100, up, right, down, left)
                row.append(tile)
            self.tiles.append(row)

    def draw_walls(self, win):
        for row in self.tiles:
            for tile in row:
                tile.draw(win)
