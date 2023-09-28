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
from math import pi


class Map(Object):
    point_radius = 8
    view_size = [400, 400]
    """
    Initialize a map object.

    Args:
        x (int): The x-coordinate of the map.
        y (int): The y-coordinate of the map.
        game: The game object.
        window: The window object.
        width (int, optional): The width of the map (default is 200).
        height (int, optional): The height of the map (default is 200).
        car_x (int, optional): The x-coordinate of the car (default is 100).
        car_y (int, optional): The y-coordinate of the car (default is 100).

    """

    def __init__(self, x, y, game, window, width=200, height=200, car_x=100, car_y=100):
        super().__init__(x, y, game, window, width, height)
        self.car_x = car_x
        self.car_y = car_y
        self.map_image = self.game.image.load("setup/images/Track.png")
        self.font = self.game.font.SysFont("Times New Roman", 20)

        self.rap = self.width / self.view_size[0]

        self.frame = self.game.Rect(
            0, 0, self.surface.get_width(), self.surface.get_height()
        )

        self.view_x = self.car_x - self.view_size[0] / 2
        self.view_y = self.car_y - self.view_size[1] / 2

        self.clamp()
        self.point_x = abs(self.car_x - self.view_x)
        self.point_y = abs(self.car_y - self.view_y)

        self.view = self.map_image.subsurface(
            self.view_x, self.view_y, self.view_size[0], self.view_size[1]
        )
        self.view = self.game.transform.scale(self.view, (self.width, self.height))

    def clamp(self):
        """
        Ensure the map view and car position remain within valid boundaries.

        This method adjusts the map view and car position to ensure they do not go beyond
        the boundaries of the map image.

        """
        if self.view_x < 0:
            self.view_x = 0
        elif self.view_x + self.view_size[0] > self.map_image.get_width():
            self.view_x = self.map_image.get_width() - self.view_size[0]

        if self.view_y < 0:
            self.view_y = 0
        elif self.view_y + self.view_size[1] > self.map_image.get_height():
            self.view_y = self.map_image.get_height() - self.view_size[1]

        if self.car_x - self.point_radius / self.rap < 0:
            self.car_x = self.point_radius / self.rap
        elif self.car_x + self.point_radius / self.rap > self.map_image.get_width():
            self.car_x = self.map_image.get_width() - self.point_radius / self.rap
        if self.car_y - self.point_radius / self.rap < 0:
            self.car_y = self.point_radius / self.rap
        elif self.car_y + self.point_radius / self.rap > self.map_image.get_height():
            self.car_y = self.map_image.get_height() - self.point_radius / self.rap

    def new_coordinates(self, x, y):
        """
        Update the car's coordinates on the map.

        Args:
            x (float): The new x-coordinate for the car.
            y (float): The new y-coordinate for the car.

        """
        self.car_x = x
        self.car_y = y
        self.update()

    def update(self):
        """
        Update the map view and car's position.

        This method updates the map view based on the car's position and ensures it remains
        within valid boundaries.

        """
        self.point_x = abs(self.car_x - self.view_x)
        self.point_y = abs(self.car_y - self.view_y)

        self.view_x = self.car_x - self.view_size[0] / 2
        self.view_y = self.car_y - self.view_size[1] / 2
        self.clamp()

    def draw(self):
        """
        Draw the map and car's position on the surface.

        This method renders the map view, car's position indicator, and cardinal direction
        labels on the surface.

        """
        self.view = self.map_image.subsurface(
            self.view_x, self.view_y, self.view_size[0], self.view_size[1]
        )
        self.view = self.game.transform.scale(self.view, (self.width, self.height))
        self.surface.blit(self.view, (0, 0))
        self.game.draw.rect(self.surface, (122, 122, 122), self.frame, 3)
        self.game.draw.circle(
            self.surface,
            (0, 0, 255),
            (self.rap * self.point_x, self.rap * self.point_y),
            self.point_radius,
        )
        self.game.draw.circle(
            self.surface,
            (255, 255, 255),
            (self.rap * self.point_x, self.rap * self.point_y),
            self.point_radius - 3,
        )

        north = self.font.render("X", True, (255, 255, 255))
        east = self.font.render("Y", True, (255, 255, 255))

        self.window.blit(north, (self.x + self.width / 2, self.y - 20))
        self.window.blit(east, (self.x - 20, self.y + self.height / 2))

        super().draw()
