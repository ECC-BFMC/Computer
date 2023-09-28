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

from random import choice, randint
from math import sin
from .Object import Object


class FloatingPiece(Object):
    A = 5
    w = 0.09
    """
    Initialize a car object.

    Args:
        x (int): The x-coordinate of the car.
        y (int): The y-coordinate of the car.
        game: The game object.
        window: The window object.
        width (int, optional): The width of the car (default is 100).
        height (int, optional): The height of the car (default is 60).

    """

    def __init__(self, x, y, game, window, width=100, height=60):
        super().__init__(x, y, game, window, width, height)
        self.dx = randint(1, 2)
        image1 = self.game.image.load("objects/images/blue_car.png")
        image1 = self.game.transform.scale(image1, (self.width, self.height))
        image2 = self.game.image.load("objects/images/yellow_car.png")
        image2 = self.game.transform.scale(image2, (self.width, self.height))
        self.image = choice([image1, image2])
        self.color = choice(["Yellow", "Red"])
        self.surface = self.game.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 0, 0))

    def update(self):
        """
        Update the car's position.

        This method updates the car's x and y coordinates based on a predefined formula.

        """
        self.x += self.dx
        self.y += self.A * sin(self.w * self.x)

    def draw(self):
        """
        Draw the car on the surface.

        This method blits the car's image onto the surface.

        """
        self.surface.blit(self.image, (0, 0))
        super().draw()
