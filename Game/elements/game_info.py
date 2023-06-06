from pygame import font as pg_font, draw, Surface

class info:
    def __init__(self, struct, win):
        self.struct = struct
        self.WIDTH = struct.WIDTH
        self.HEIGHT = struct.HEIGHT  # Assuming struct.HEIGHT holds the window height
        self.WIN = win

    def __clear(self):
        bottom_info_area = Surface((self.WIDTH, 100))  # Create a new surface with the width of the window and height of 100
        bottom_info_area.fill((0, 0, 0))  # Fill the surface with black
        self.WIN.blit(bottom_info_area, (0, self.HEIGHT - 100))  # Draw the surface at the bottom of the window

    def show(self):
        self.__clear()  # Clear the previous info
        pg_font.init()
        font = pg_font.SysFont('Arial', 30)
        current_player_color = self.struct.PLAYER_COLORS[self.struct.current_player]
        player_color_text = font.render("Current Player:", True, (255, 255, 255))
        wall_remaining_text = font.render(f"Wall Remaining: {str(self.struct.remaining_walls[self.struct.current_player])}", True, (255, 255, 255))

        # Define the y positions statically
        y_position_player_color = self.HEIGHT - 90
        y_position_wall_remaining = self.HEIGHT - 50

        # Define the x positions for the text and the color rectangle
        x_position_text = self.WIDTH // 2 - player_color_text.get_width() // 2
        x_position_rect = x_position_text + player_color_text.get_width() + 10  # 10 pixels gap from the end of the text

        # Draw the player color rectangle
        draw.rect(self.WIN, current_player_color, (x_position_rect, y_position_player_color, 50, 30))

        self.WIN.blit(player_color_text, (x_position_text, y_position_player_color))
        self.WIN.blit(wall_remaining_text, (x_position_text, y_position_wall_remaining))
