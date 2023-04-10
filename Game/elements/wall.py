import pygame

class Wall:
    def __init__(self, x, y, type,active=True):
        self.x = x
        self.y = y
        self.type = type
        self.active = active

        if type == "horizontal":
            self.width = 240
            self.height = 20
        elif type == "vertical":
            self.width = 20
            self.height = 240

        self.graphic = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.graphic)

    def get_rect(self):
        return self.graphic

    def hover(self, win, color):
        pygame.draw.rect(win, color, self.graphic)


