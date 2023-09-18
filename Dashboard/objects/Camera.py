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
import cv2
import numpy as np


class Camera(Object):
    def __init__(self, x, y, game, window, width=220, height=120):
        super().__init__(x, y, game, window, width, height)
        image1 = self.game.image.load("setup/images/BFMC.png")
        self.frame = self.game.transform.scale(image1, (self.width, self.height))
        self.font = self.game.font.Font(None, 25)
        self.rectangle = self.game.Rect(x, y, self.width, self.height)
        self.on = False

    def change_frame(self, newFrame):
        newFrame = cv2.imdecode(newFrame, cv2.IMREAD_COLOR)
        newFrame = np.rot90(newFrame)
        newFrame = np.flip(newFrame, axis=0)
        newSurface = self.game.surfarray.make_surface(newFrame)
        self.frame = self.game.transform.scale(newSurface, (self.width, self.height))

    def draw(self):
        self.surface.fill(0)
        self.surface.blit(self.frame, (0, 0))
        super().draw()

    def conn_lost(self):
        image1 = self.game.image.load("objects/images/BFMC.png")
        self.frame = self.game.transform.scale(image1, (self.width, self.height))

    def update(self):
        super().update()
