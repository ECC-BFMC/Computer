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


class ScrollSlider(Object):
    def __init__(
        self,
        x,
        y,
        maximum,
        game,
        window,
        width=120,
        height=20,
    ):
        super().__init__(x, y, game, window, width, height)
        self.minimum = 0
        self.maximum = maximum
        self.current_value = 0
        self.slider_width = self.width
        self.slider_height = self.height
        self.pin_height = 20
        self.slider_x = width + self.x
        self.slider_y = self.y
        self.pin_range_start = 0
        self.pin_range_end = 8
        self.pin_range_y_start = 0
        self.pin_range_y_end = 0
        self.pin_y = self.slider_y
        self.rectangle = self.game.Rect(
            self.slider_x, self.slider_y, self.width, self.height
        )

    def colliding(self, mousePos):
        if self.rectangle.collidepoint(mousePos):
            (x, y) = mousePos
            normalized_y = 1 - (y - self.slider_y) / (
                self.slider_height - self.pin_height
            )
            normalized_y = max(0, min(1, normalized_y))
            self.current_value = self.minimum + normalized_y * (
                self.maximum - self.minimum
            )

    def mouseWheelInteract(self, mousePos, dif):
        if self.rectangle.collidepoint(mousePos):
            if (
                self.game.mouse.get_pos()[0] >= self.slider_x
                and self.game.mouse.get_pos()[0] <= self.slider_x + self.slider_width
            ):
                self.current_value += dif

    def draw(self):
        self.update()
        self.game.draw.rect(
            self.window,
            (0, 0, 0),
            (self.slider_x, self.slider_y, self.slider_width, self.slider_height),
        )
        self.game.draw.rect(
            self.window,
            (255, 0, 0),
            (
                self.slider_x,
                self.pin_y,
                self.slider_width,
                self.pin_range_y_start - self.pin_range_y_end + 20,
            ),
        )
        super().draw()

    def calculate_pin_position(self, value):
        normalized_value = (value - self.minimum) / (self.maximum - self.minimum)
        return self.slider_y + (1 - normalized_value) * (
            self.slider_height - self.pin_height
        )

    def update(self):
        self.current_value = max(self.minimum, min(self.maximum, self.current_value))
        self.pin_range_y_start = self.calculate_pin_position(self.pin_range_start)
        dif = self.pin_range_end - self.pin_range_start
        if self.current_value - dif < self.minimum:
            self.current_value = self.minimum + dif
        self.pin_range_y_end = self.calculate_pin_position(self.pin_range_end)
        self.pin_y = self.calculate_pin_position(self.current_value)
        self.current_value = round(self.current_value)
