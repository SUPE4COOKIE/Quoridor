from pygame.display import set_mode, set_caption, update

class NewWindow:
    def __init__(self, width: int, height: int, title: str) -> None:
        # Set the necessary attributes
        self.width = width
        self.height = height
        self.title = title
        self.window = set_mode((self.width, self.height))
        set_caption(self.title)

    def update(self) -> None:
        """
        Updates the window
        """
        update()

    def get_window(self) -> None:
        """
        Returns the window
        """
        return self.window
