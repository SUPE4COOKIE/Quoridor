from Game.elements.tile import Tile
from Game.elements.wall import Wall
from Game.elements.pawn import Pawn
class Board:
    def __init__(self, rows, cols,players):
        self.rows = rows
        self.cols = cols
        self.players = players
        self.tiles = []
        self.__init_pawns()
        self.tile_size = 115
        self.__init_tiles()


    def __init_tiles(self):
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
            
                # Setup wall activity
                top_active = not (i == 0)
                right_active = not (j == self.cols - 1)
                bottom_active = not (i == self.rows - 1)
                left_active = not (j == 0)
    
                # Setup Wall object, reusing if available
                up = self.tiles[i - 1][j].wall_down if i > 0 else Wall(j * self.tile_size, i * self.tile_size, "horizontal", active=top_active)
                right = Wall((j + 1) * self.tile_size, i * self.tile_size, "vertical", active=right_active)
                down = Wall(j * self.tile_size, (i + 1) * self.tile_size, "horizontal", active=bottom_active)
                left = row[-1].wall_right if j > 0 else Wall(j * self.tile_size, i * self.tile_size, "vertical", active=left_active)
    
                tile = Tile(j * self.tile_size + 20, i * self.tile_size + 20,(j,i), up, right, down, left)
                row.append(tile)
    
            self.tiles.append(row)


    def __init_pawns(self):
        self.pawns = []
        for player_count in range(self.players):
            if player_count == 0:
                x = self.cols // 2
                y = self.rows - 1
                color = (255, 0, 0)
            elif player_count == 1:
                x = self.cols // 2
                y = 0
                color = (0, 0, 255)
            elif player_count == 2:
                x = self.cols - 1
                y = self.rows // 2
                color = (0, 255, 0)
            else:
                x = 0
                y = self.rows // 2
                color = (255, 255, 0)
            self.pawns.append(Pawn(x, y, color))


    def draw_walls(self, win): #TODO : Change the name
        for row in self.tiles:
            for tile in row:
                tile.draw(win)
                for pawn in self.pawns:
                    if pawn.x == tile.x_index and pawn.y == tile.y_index:
                        tile.pawn = pawn
                    elif tile.pawn is not None and (pawn.x != tile.x_index or pawn.y != tile.y_index):
                        tile.pawn = None

    def draw_pawns(self, win):
        self.win = win
        for pawn in self.pawns:
            pawn.draw_on_tile(win, self.tiles[pawn.y][pawn.x])

    def get_neighbor(self, x, y, orientation):
        if orientation == 1:
            if y < 6: #TODO : hard coded 6
                return self.tiles[y+1][x].GetWalls()[orientation]
            else:
                return self.tiles[y-1][x].GetWalls()[orientation]
        else:
            if x < 6:
                return self.tiles[y][x+1].GetWalls()[orientation]
            else:
                return self.tiles[y][x-1].GetWalls()[orientation]
    
    def is_move_possible(self, tile, player_number):
        pawn = self.pawns[player_number]
        diff_x = abs(tile.x_index - pawn.x)
        diff_y = abs(tile.y_index - pawn.y)

        is_horizontal_move = (diff_x == 1) and (tile.y_index == pawn.y)
        is_vertical_move = (diff_y == 1) and (tile.x_index == pawn.x)

        # check if there's a wall in the way
        if is_horizontal_move:
            if pawn.x < tile.x_index: # moving right
                return not tile.wall_left.placed
            else: # moving left
                return not tile.wall_right.placed
        elif is_vertical_move:
            if pawn.y < tile.y_index: # moving down
                return not tile.wall_up.placed
            else: # moving up
                return not tile.wall_down.placed

        if is_horizontal_move or is_vertical_move:
            return True

        return False

    def is_wall_placeable(self, tile, orientation):

        neighbor = self.get_neighbor(tile.x_index, tile.y_index, orientation)

        if neighbor.placed:
            return False
        
        if orientation == 1 and tile.wall_down.placed:
            return False
        elif orientation == 2 and tile.wall_right.placed:
            return False
        
        return True
            
