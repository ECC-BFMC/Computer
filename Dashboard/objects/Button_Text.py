import pygame
from objects.Object import Object


class Button_Text(Object):

    """
    Initialize a toggle button.

    Args:
        x (int): The x-coordinate of the button.
        y (int): The y-coordinate of the button.
        game: The game object.
        window: The window object.
        text (str): The text label for the button.
        width (int, optional): The width of the button (default is 70).
        height (int, optional): The height of the button (default is 25).

    """

    on = False
    states = {}

    def sendMessage(self):
        """
        Send messages based on the content of the dictionary.

        This method iterates through the dictionary and sends messages for each key-value pair.
        Each message consists of an "action" and a "value" taken from the dictionary.

        """
        for key, value in self.dictionary.items():
            self.pipe.send({"action": key, "value": value})

    def __init__(self, x, y, game, window, text, width=70, height=25):
        super().__init__(x, y, game, window, width, height)
        self.font = self.game.font.Font(None, 25)
        self.text_on = "ON"
        self.text_off = "OFF"
        self.text_color = (0, 0, 0)
        self.rect_color = (130, 130, 130)
        self.rectangle = self.game.Rect(x, y, self.width, self.height)
        self.text = text

    def colliding(self, mousePos):
        """
        Check if the mouse position collides with the button's rectangle.

        Args:
            mousePos (tuple): The mouse position as a tuple (x, y).

        Returns:
            bool: True if the mouse position collides with the button's rectangle, False otherwise.
        """
        if self.rectangle.collidepoint(mousePos):
            return True
        else:
            return False

    def draw(self):
        """
        Draw the toggle button on the surface.

        This method fills the surface with a background color, draws the button's rectangular
        region with its defined color, and renders the button's text label in the center.

        """
        self.surface.fill(0)
        self.game.draw.rect(
            self.surface, self.rect_color, (0, 0, self.width, self.height)
        )
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.width // 2 - text_surface.get_width() // 2
        text_y = self.height // 2 - text_surface.get_height() // 2
        self.surface.blit(text_surface, (text_x, text_y))
        super().draw()

    def update(self):
        super().update()
