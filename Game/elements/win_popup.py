import pygame
import subprocess
from Game.elements.window import NewWindow

class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), highlight_color=(189, 189, 189), function=None, params=None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.highlight_color = highlight_color
        self.function = function
        self.params = params
        self.text = text
        if self.text:
            font = pygame.font.Font(None, 36)
            self.text_surf = font.render(self.text, True, (255, 255, 255))
            self.text_rect = self.text_surf.get_rect(center=(width/2, height/2))
            self.image.blit(self.text_surf, self.text_rect)
    
    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(self.highlight_color)
            if mouse_up:
                if self.params:
                    self.function(*self.params)
                else:
                    self.function()
        else:
            self.image.fill(self.color)
        if self.text:
            self.image.blit(self.text_surf, self.text_rect)

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class WinPopup:
    def __init__(self, ReplayFile) -> None:
        self.WIDTH = 300
        self.HEIGHT = 150
        self.REPLAY_FILE = ReplayFile
        self.WINDOW = NewWindow(self.WIDTH, self.HEIGHT, "Game Over").get_window()

        pygame.font.init()
        self.FONT = pygame.font.Font(None, 36)
        self.BACKGROUND_COLOR = (250,237,205)
        self.CONTENT_COLOR = (212, 163, 115)
        self.running = True

        self.quit_button = Button(50, 100, 90, 40, 'Quit', function=lambda: (setattr(self, 'running', False)))
        self.replay_button = Button(160, 100, 90, 40, 'Replay', function=self.__replay)

    def display(self, message:str) -> None:
        while self.running:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_up = True

            self.WINDOW.fill(self.BACKGROUND_COLOR)

            text = self.FONT.render(message, True, self.CONTENT_COLOR)
            text_rect = text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2 - 40))
            self.WINDOW.blit(text, text_rect)

            mouse_pos = pygame.mouse.get_pos()

            self.quit_button.update(mouse_pos, mouse_up)
            self.quit_button.draw(self.WINDOW)

            self.replay_button.update(mouse_pos, mouse_up)
            self.replay_button.draw(self.WINDOW)

            pygame.display.update()

    def __replay(self):
        subprocess.Popen(["python", self.REPLAY_FILE])
        self.running = False
