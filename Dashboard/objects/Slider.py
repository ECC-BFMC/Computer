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


class Slider(Object):
    """
    Initialize a numerical input slider.
    Args:
        x (int): The x-coordinate of the slider.
        y (int): The y-coordinate of the slider.
        precision (int): The precision of the numerical value.
        defValue (float): The default value of the slider.
        minimum (float): The minimum value the slider can represent.
        maximum (float): The maximum value the slider can represent.
        game: The game object.
        window: The window object.
        width (int, optional): The width of the slider (default is 120).
        height (int, optional): The height of the slider (default is 20).
    """

    def __init__(
        self,
        x,
        y,
        precision,
        defValue,
        minimum,
        maximum,
        game,
        window,
        width=120,
        height=20,
    ):
        super().__init__(x, y, game, window, width, height)
        self.minimum = minimum
        self.maximum = maximum
        self.precision = precision
        self.defValue = float(defValue)
        self.slider_width = 100
        self.slider_height = 10
        self.slider_x = width + self.x - self.slider_width - 40
        self.slider_y = height + self.y
        self.rectangle = self.game.Rect(
            self.slider_x, self.slider_y, self.width, self.height
        )

    def colliding(self, mousePos):
        """
        Check if the mouse cursor collides with the slider.

        Args:
            mousePos (tuple): The mouse cursor's position (x, y).

        """
        if self.rectangle.collidepoint(mousePos):
            (x, y) = mousePos
            normalized_x = (x - self.slider_x) / self.slider_width
            number = format(
                (self.minimum + normalized_x * (self.maximum - self.minimum)),
                f".{self.precision}f",
            )
            self.defValue = str(number)

    def draw(self):
        """
        Draw the slider on the window.

        """
        self.game.draw.rect(
            self.window,
            (255, 255, 255),
            (
                self.slider_x,
                self.slider_y,
                self.slider_width,
                self.slider_height,
            ),
        )
        handle_x = (
            self.slider_x
            + (float(self.defValue) - self.minimum)
            / (self.maximum - self.minimum)
            * self.slider_width
        )

        self.game.draw.circle(
            self.window,
            (255, 0, 0),
            (int(handle_x), self.slider_y + 5),
            5,
        )
        super().draw()

    def update(self):
        pass
