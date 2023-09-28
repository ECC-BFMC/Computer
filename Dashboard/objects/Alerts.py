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
import json


class Alerts(Object):
    """
    Initialize an instance of the class.

    Args:
        x (int): The x-coordinate of the instance.
        y (int): The y-coordinate of the instance.
        game: The game object.
        window: The window object.
        size (int, optional): The size of the instance (default is 300).
    """

    def __init__(self, x, y, game, window, size=300):
        self.square = size / 5
        height = self.square * 5
        self.seconds_fadeaway = 3.0
        self.lights = {}
        super().__init__(x, y, game, window, size, height)
        self.frame = self.game.Rect(
            0, 0, self.surface.get_width(), self.surface.get_height()
        )
        self.read()
        for name in self.names.keys():
            # self.values[name] = True
            image = self.game.image.load("setup/images/lights/" + name + ".png")
            image = self.game.transform.scale(image, (self.square, self.square))
            self.lights[name] = image

    def update(self, timePassed):
        """
        Update timers associated with named actions and set values to "False" when timers expire.

        Args:
            timePassed (float): The time passed, in seconds.

        """
        for key, value in self.names.items():
            self.names[key] = value - timePassed
            if self.names[key] < 0:
                self.values[key] = "False"

    def setValues(self, value):
        """
        Set a named value to "True" and initialize its associated timer.

        Args:
            value (str): The name of the value to be set.

        """
        self.values[value] = "True"
        self.names[value] = self.seconds_fadeaway

    def draw(self):
        """
        Draw the lights on the surface.

        This method fills the surface with a background color and draws lights that are set
        to "True" based on their timers and alpha values.

        """
        self.surface.fill(0)
        i = 0
        j = 0
        for name in self.names:
            if self.values[name] == "True":
                self.lights[name].set_alpha(
                    255 / self.seconds_fadeaway * self.names[name]
                )
                self.surface.blit(self.lights[name], (i * self.square, j * self.square))
            if i == 4:
                i = 0
                j += 1
            else:
                i += 1

        self.game.draw.rect(self.surface, (122, 122, 122), self.frame, 3)
        super().draw()

    def read(self):
        """
        Read data from a JSON file to initialize names and values.

        This method reads data from a JSON file located at "setup/Alerts.json" to initialize
        the `names` and `values` attributes.

        """
        with open("setup/Alerts.json", "r") as f:
            self.data = json.load(f)
        self.names = self.data["names"]
        self.values = self.data["values"]
