from typing import List, Tuple
from Game.elements.wall import Wall
import pygame


class Tile:
    def __init__(self, x: int, y: int, size: int, index: Tuple[int, int],
                 wall_up: Wall, wall_right: Wall, wall_down: Wall, wall_left: Wall, wall_size: int) -> None:
        """
        Initializes a Tile instance.

        :param x: The x-coordinate of the tile's position.
        :param y: The y-coordinate of the tile's position.
        :param size: The size of the tile.
        :param index: A tuple representing the index of the tile in the grid.
        :param wall_up: The Wall instance above the tile.
        :param wall_right: The Wall instance to the right of the tile.
        :param wall_down: The Wall instance below the tile.
        :param wall_left: The Wall instance to the left of the tile.
        """
        self.x = x
        self.y = y
        self.x_index = index[0]
        self.y_index = index[1]

        # Reduce size by wall_size to add padding
        self.size = size - wall_size

        # Instances of walls surrounding the tile
        self.wall_up = wall_up
        self.wall_right = wall_right
        self.wall_down = wall_down
        self.wall_left = wall_left

        # Pawn that might be placed on the tile
        self.pawn = None

        # Colors for the tile
        self.COLOR = (250, 237, 205)
        self.HOVER_COLOR = (219, 209, 186)

    def draw(self, win: pygame.Surface) -> None:
        """
        Draws the tile on the given surface along with its walls.

        :param win: The Pygame surface to draw the tile on.
        """
        # Draw the tile itself as a rectangle
        self.rect = pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.size, self.size))
        self.win = win
        self.draw_walls(win, [True, True, True, True])

    def draw_walls(self, win: pygame.Surface, walls_to_show: List[bool]) -> None:
        """
        Draws the walls surrounding the tile on the given surface.

        :param win: The Pygame surface to draw the walls on.
        :param walls_to_show: A list of booleans representing which walls to show.
        """
        walls = self.GetWalls()
        for i in range(len(walls_to_show)):
            if walls_to_show[i] and walls[i] is not None:
                walls[i].draw(win)

    def hover(self) -> None:
        """
        Highlights the tile by drawing it with hover color.
        """
        pygame.draw.rect(self.win, self.HOVER_COLOR, self.rect)

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle representing the tile.

        :return: A pygame.Rect object representing the tile.
        """
        return self.rect

    def GetWalls(self) -> List[Wall]:
        """
        Returns a list of the Wall instances surrounding the tile.

        :return: A list containing the Wall instances in the order: up, right, down, left.
        """
        return [self.wall_up, self.wall_right, self.wall_down, self.wall_left]
