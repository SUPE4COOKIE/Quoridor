from typing import Any
from pygame import font as pg_font, draw, Surface


class Info:
    def __init__(self, struct: Any, win: Surface) -> None:
        """
        Initialize the Info class which displays information at the bottom of the game window.

        :param struct: An object containing game configuration data.
        :param win: The Pygame Surface to draw the information on.
        """
        self.struct = struct
        self.WIDTH = struct.WIDTH
        self.HEIGHT = struct.HEIGHT  # Assuming struct.HEIGHT holds the window height
        self.WIN = win
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.TEXT_COLOR = (255, 255, 255)
        pg_font.init()
        self.font = pg_font.SysFont('Arial', 30)

    def __clear(self) -> None:
        """
        Clear the bottom area of the window where the information is displayed.
        """
        # Create a new surface with the width of the window and height of 100
        bottom_info_area = Surface((self.WIDTH, 100))
        # Fill the surface with black color
        bottom_info_area.fill(self.BACKGROUND_COLOR)
        # Draw the surface at the bottom of the window
        self.WIN.blit(bottom_info_area, (0, self.HEIGHT - 100))

    def show(self) -> None:
        """
        Show the information (current player color and number of walls remaining) at the bottom of the window.
        """
        # Clear the previous info
        self.__clear()

        # Get current player color
        current_player_color = self.struct.PLAYER_COLORS[self.struct.current_player]

        # Render text surfaces
        player_color_text = self.font.render("Current Player:", True, self.TEXT_COLOR)
        wall_remaining_text = self.font.render(f"Walls Remaining: {str(self.struct.remaining_walls[self.struct.current_player])}", True, self.TEXT_COLOR)

        # Define the y positions statically
        y_position_player_color = self.HEIGHT - 90
        y_position_wall_remaining = self.HEIGHT - 50

        # Define the x positions for the text and the color rectangle
        x_position_text = self.WIDTH // 2 - player_color_text.get_width() // 2
        x_position_rect = x_position_text + player_color_text.get_width() + 10  # 10 pixels gap from the end of the text

        # Draw the rectangle representing the current player's color
        draw.rect(self.WIN, current_player_color, (x_position_rect, y_position_player_color, 50, 30))

        # Blit text surfaces onto the window surface
        self.WIN.blit(player_color_text, (x_position_text, y_position_player_color))
        self.WIN.blit(wall_remaining_text, (x_position_text, y_position_wall_remaining))
