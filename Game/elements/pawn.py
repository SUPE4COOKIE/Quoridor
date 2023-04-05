from pygame import Surface, draw, Rect, SRCALPHA , display
from pygame import Color


class Pawn:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = Surface((self.width, self.height), SRCALPHA)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.draw()

    def draw(self):
        draw.rect(self.surface, self.color, self.rect)

    def get_surface(self):
        return self.surface

    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_color(self):
        return self.color

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_color(self, color):
        self.color = color

    def set_rect(self, rect):
        self.rect = rect

    def set_surface(self, surface):
        self.surface = surface

    def update(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.surface = Surface((self.width, self.height), SRCALPHA)
        self.draw()

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height}, color: {self.color}'
