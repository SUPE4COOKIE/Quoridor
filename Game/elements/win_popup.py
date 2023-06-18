import pygame
import subprocess
from typing import Tuple, Optional, Any, Callable, List
from Game.elements.window import NewWindow


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: Optional[str] = None,
                 color: Tuple[int, int, int] = (73, 73, 73),
                 highlight_color: Tuple[int, int, int] = (189, 189, 189),
                 function: Optional[Callable] = None, params: Optional[List[Any]] = None) -> None:
        """
        Initializes a Button instance.
        
        :param x: The x-coordinate of the button.
        :param y: The y-coordinate of the button.
        :param width: The width of the button.
        :param height: The height of the button.
        :param text: The text displayed on the button.
        :param color: The normal color of the button.
        :param highlight_color: The color when the button is highlighted (e.g. mouse hover).
        :param function: The function to be called when the button is clicked.
        :param params: The parameters to be passed to the function when called.
        """
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlight_color = highlight_color
        self.function = function
        self.params = params
        self.text = text
        
        # If text is provided, render it on the button
        if self.text:
            font = pygame.font.Font(None, 36)
            self.text_surf = font.render(self.text, True, (255, 255, 255))
            self.text_rect = self.text_surf.get_rect(center=(width/2, height/2))
            self.image.blit(self.text_surf, self.text_rect)

    def update(self, mouse_pos: Tuple[int, int], mouse_up: bool) -> None:
        """
        Updates the state of the button based on mouse position and click.
        
        :param mouse_pos: The current position of the mouse cursor.
        :param mouse_up: A boolean indicating if the mouse button was released.
        """
        # If mouse is over the button
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.highlight_color)
            # If the button is clicked
            if mouse_up:
                if self.params:
                    self.function(*self.params)
                else:
                    self.function()
        else:
            self.image.fill(self.color)
            
        # Re-apply text to keep it visible on color change
        if self.text:
            self.image.blit(self.text_surf, self.text_rect)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the button on the given screen.
        
        :param screen: The Pygame surface to draw the button on.
        """
        screen.blit(self.image, self.pos)


class WinPopup:
    def __init__(self, ReplayFile: str) -> None:
        """
        Initializes a WinPopup instance.
        
        :param ReplayFile: The file path for replaying the game.
        """
        self.WIDTH = 300
        self.HEIGHT = 150
        self.REPLAY_FILE = ReplayFile
        self.WINDOW = NewWindow(self.WIDTH, self.HEIGHT, "Game Over").get_window()

        pygame.font.init()
        self.FONT = pygame.font.Font(None, 36)
        self.BACKGROUND_COLOR = (250, 237, 205)
        self.CONTENT_COLOR = (212, 163, 115)
        self.running = True

        # Initialize the quit and replay buttons
        self.quit_button = Button(50, 100, 90, 40, 'Quit', function=lambda: setattr(self, 'running', False))
        self.replay_button = Button(160, 100, 90, 40, 'Replay', function=self.__replay)

    def display(self, message: str) -> None:
        """
        Displays the popup window with the given message.
        
        :param message: The message to be displayed on the popup window.
        """
        # Main loop for the popup window
        while self.running:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_up = True

            # Fill the window with background color
            self.WINDOW.fill(self.BACKGROUND_COLOR)

            # Render the message text
            text = self.FONT.render(message, True, self.CONTENT_COLOR)
            text_rect = text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2 - 40))
            self.WINDOW.blit(text, text_rect)

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Update and draw the buttons
            self.quit_button.update(mouse_pos, mouse_up)
            self.quit_button.draw(self.WINDOW)

            self.replay_button.update(mouse_pos, mouse_up)
            self.replay_button.draw(self.WINDOW)

            # Update the display
            pygame.display.update()

    def __replay(self) -> None:
        """
        Replays the game by executing the replay file.
        """
        # Run the replay file in a new process
        subprocess.Popen(["python", self.REPLAY_FILE])
        self.running = False
