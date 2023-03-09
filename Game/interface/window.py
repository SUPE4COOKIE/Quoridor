from pygame.display import set_mode, set_caption, set_icon , update , init

class NewWindow:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = set_mode((self.width, self.height))
        set_caption(self.title)

    def update(self):
        update()

    def get_window(self):
        return self.window
