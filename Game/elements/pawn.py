from pygame.draw import circle
import pygame
from typing import Tuple, Union


class Pawn:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Initializes a Pawn instance.

        :param x: The x-coordinate of the pawn's position in the grid.
        :param y: The y-coordinate of the pawn's position in the grid.
        :param color: A tuple representing the RGB color of the pawn.
        """
        self.x = x
        self.y = y
        self.color = color
        self.pawn = None
        self.surface = None

    def draw_on_tile(self, surface: pygame.Surface, tile) -> None:
        """
        Draws the pawn on a given tile.

        :param surface: The Pygame surface to draw the pawn on.
        :param tile: The Tile object representing the tile the pawn is on.
        """
        self.surface = surface
        # Draw the Cirlce representing the pawn in the middle of the Tile
        self.pawn = circle(surface, self.color, (tile.x + tile.size // 2, tile.y + tile.size // 2), tile.size // 4)

    def move(self, tile) -> None:
        """
        Moves the pawn to the given tile, or jumps over if the tile is occupied.

        :param tile: The Tile object representing the destination tile.
        """
        if tile.pawn is None: # If the tile is empty, move to it
            self.x = tile.x_index
            self.y = tile.y_index
        else:
            # Jump over the tile if there is already a pawn
            if self.x == tile.x_index:
                if self.y < tile.y_index:
                    self.y = tile.y_index + 1
                else:
                    self.y = tile.y_index - 1
            elif self.y == tile.y_index:
                if self.x < tile.x_index:
                    self.x = tile.x_index + 1
                else:
                    self.x = tile.x_index - 1

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the grid position of the pawn.

        :return: A tuple representing the (x, y) grid position of the pawn.
        """
        return self.x, self.y

    def get_circle(self) -> Union[pygame.Surface, None]:
        """
        Returns the Pygame Surface object representing the pawn, if it has been drawn.

        :return: The Pygame Surface object representing the pawn, or None if it hasn't been drawn.
        """
        return self.pawn
