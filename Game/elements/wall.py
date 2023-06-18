import pygame
from typing import Literal


class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, type: Literal["horizontal", "vertical"], active: bool = True) -> None:
        """
        Initializes a Wall instance.

        :param x: The x-coordinate of the wall's position.
        :param y: The y-coordinate of the wall's position.
        :param width: The width of the wall.
        :param height: The height of the wall.
        :param type: The type of wall, either "horizontal" or "vertical".
        :param active: A boolean indicating whether the wall is active. (not active on the borders)
        """
        self.x = x
        self.y = y
        self.type = type
        self.active = active
        self.placed = False

        # Colors for different states of the wall
        self.PLACED_COLOR = (124, 86, 47)
        self.UNPLACED_COLOR = (212, 163, 115)
        self.HOVER_COLOR = (204, 213, 174)

        # Set the dimensions depending on the type of wall
        if type == "horizontal":
            self.width = width
            self.height = height
        elif type == "vertical":
            self.width = height
            self.height = width

        # Create a rectangle representing the wall
        self.graphic = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win: pygame.Surface) -> None:
        """
        Draws the wall on the given surface.

        :param win: The Pygame surface to draw the wall on.
        """
        # Choose the color based on whether the wall is placed
        color = self.PLACED_COLOR if self.placed else self.UNPLACED_COLOR
        pygame.draw.rect(win, color, self.graphic)

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rectangle representing the wall.

        :return: A pygame.Rect object representing the wall.
        """
        return self.graphic

    def hover(self, win: pygame.Surface) -> None:
        """
        Highlights the wall by drawing it with hover color.

        :param win: The Pygame surface to draw the hover effect on.
        """
        pygame.draw.rect(win, self.HOVER_COLOR, self.graphic)

    def place(self) -> None:
        """
        Marks the wall as placed and deactivates it.
        """
        self.placed = True
        self.active = False

    def remove(self) -> None:
        """
        Removes the wall and sets it as active.
        """
        self.placed = False
        self.active = True
