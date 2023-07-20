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

class Table(Object):

    title = "Messages"
    found = False
    rows = []
    def __init__(self, x, y, game, window, width=200, height=200):
        super().__init__(x, y, game, window, width, height)
        self.frame = self.game.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

        self.font = self.game.font.SysFont(None, 40)      
        with open('utils/CarData.json', 'r') as f:
            self.data = json.load(f)

    def update(self):
        pass

    def get_image(self, image):
        self.image = image
        self.found = True
        
    def draw(self):
        
        self.game.draw.rect(self.surface, (255, 0, 0), self.frame, 3)
        # text = self.font.render("CAN SIGNALS", True, (255, 0, 0))
        # self.surface.blit(text, (10, 10))
        if self.found:
            self.surface.blit(self.image, (10,30))
        super().draw()
        
    
    
