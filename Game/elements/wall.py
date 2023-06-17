import pygame

class Wall:
    def __init__(self, x, y,width,height, type,active=True):
        self.x = x
        self.y = y
        self.type = type
        self.active = active
        self.placed = False
        self.PLACED_COLOR = (124, 86, 47)
        self.UNPLACED_COLOR = (212, 163, 115)
        self.HOVER_COLOR = (204, 213, 174)


        if type == "horizontal":
            self.width = width
            self.height = height
        elif type == "vertical":
            self.width = height
            self.height = width


        self.graphic = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, win):
        if self.placed:
            pygame.draw.rect(win, self.PLACED_COLOR, self.graphic)
        else:
            pygame.draw.rect(win, self.UNPLACED_COLOR, self.graphic)

    def get_rect(self):
        return self.graphic

    def hover(self, win):
        pygame.draw.rect(win, self.HOVER_COLOR, self.graphic)
    
    def click(self): # TODO : rename to place wall
        self.placed = True
        self.active = False
    
    def remove(self):
        self.placed = False
        self.active = True


