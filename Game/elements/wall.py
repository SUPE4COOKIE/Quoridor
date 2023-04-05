import pygame

class Wall:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y

        if type == "horizontal":
            self.width = 100
            self.height = 10
        elif type == "vertical":
            self.width = 10
            self.height = 100

        self.graphic = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.graphic)

    def get_rect(self):
        return self.graphic

    def hover(self, win, color):
        pygame.draw.rect(win, color, self.graphic)

