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

# The Object class is the type of object that will be drawn inside the states,
# such as the speedometer, the Sign Table, the Alerts, the Map, etc.


class Object:
    # The object could also have liniar speeds, but they are initialized with 0
    # for a generic object.
    dx = 0
    dy = 0
    """
    Initialize a basic rectangular object.

    Args:
        x (int): The x-coordinate of the object.
        y (int): The y-coordinate of the object.
        game: The game object.
        window: The window object.
        width (int, optional): The width of the object (default is 10).
        height (int, optional): The height of the object (default is 10).

    """

    # As any other entity of the U.I., the Object has a width, a height, it connects
    # to the game and the surface to draw on (the window), and it as its own surface
    def __init__(self, x, y, game, window, width=10, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.window = window
        self.surface = self.game.Surface((width, height))
        self.focused = False
        self.switched = True

    # movement of the object
    def update(self):
        pass

    # what is to be rendered by the object
    def draw(self):
        """
        Draw the object on the game window.

        This method blits the object's surface onto the game window at its current
        coordinates.

        """
        self.window.blit(self.surface, (self.x, self.y))
