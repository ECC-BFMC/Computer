import pygame
from objects.Object import Object


class Button_Text(Object):
    on = False
    states = {}

    def sendMessage(self):
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
        if self.rectangle.collidepoint(mousePos):
            return True
        else:
            return False

    def draw(self):
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
