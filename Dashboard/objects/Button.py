# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

from objects.Object import Object


class Button(Object):
    """
    Initialize a toggle button with images for "on" and "off" states.

    Args:
        x (int): The x-coordinate of the button.
        y (int): The y-coordinate of the button.
        pipe: The pipe for communication.
        game: The game object.
        window: The window object.
        text (str, optional): The text label for the button (default is empty).
        width (int, optional): The width of the button (default is 120).
        height (int, optional): The height of the button (default is 120).

    """

    def __init__(self, x, y, pipe, game, window, text="", width=120, height=120):
        super().__init__(x, y, game, window, width, height)
        image1 = self.game.image.load("setup/images/stop.png")
        image1 = self.game.transform.scale(image1, (self.width, self.height))
        image2 = self.game.image.load("setup/images/start.png")
        image2 = self.game.transform.scale(image2, (self.width, self.height))
        self.pipe = pipe
        self.font = self.game.font.Font(None, 25)
        self.rectangle = self.game.Rect(x, y, self.width, self.height)
        self.states = {}
        self.text = text
        self.states["on"] = image1
        self.states["off"] = image2
        self.on = False

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

        This method fills the surface with a background color and displays the appropriate image
        based on the current state ("on" or "off"). It also renders the button's text label.

        """
        self.surface.fill(0)
        if self.on:
            self.surface.blit(self.states["on"], (0, 0))
        else:
            self.surface.blit(self.states["off"], (0, 0))
        text_x = self.width // 4
        text_y = 3 * self.height // 5
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.surface.blit(text_surface, (text_x, text_y))
        super().draw()

    def update(self):
        """
        Update the toggle button's state and send control commands.

        This method updates the state of the toggle button and sends control commands based on
        whether the button is in the "on" or "off" state. It sends commands to start or stop
        the engine, reset steering, and set speed to zero.

        """
        super().update()
        if self.on is False:
            self.pipe.send({"action": "startEngine", "value": True})
            self.on = True
        else:
            self.pipe.send({"action": "startEngine", "value": False})
            self.pipe.send({"action": "steer", "value": 0})
            self.pipe.send({"action": "speed", "value": 0})
            self.on = False
