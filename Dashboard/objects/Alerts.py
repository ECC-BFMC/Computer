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

class Alerts(Object):
    
    lights = {}
    timer = 0
    count = 0

    names = ["trafficLight", "stop", "park", "cross", 
    "highwayIn", "highwayOut", "round", "oneWay", "carAhead", 
    "carParking", "pedOnRoad", "pedOnCross", "roadBlock",
    "bumpyRoad", "intersection"]

    values = {"trafficLight":True, "stop":False, "park":False, "cross":False, 
    "highwayIn":False, "highwayOut":True, "round":True, "oneWay":False, "carAhead":False, 
    "carParking":True, "pedOnRoad":False, "pedOnCross":False, "roadBlock":True,
    "bumpyRoad":True, "intersection":False}

    def __init__(self, x, y, game, window, size = 300):
        self.square = size / 5
        height = self.square * 3
        super().__init__(x, y, game, window, size, height)
        self.frame = self.game.Rect(0, 0, self.surface.get_width(), self.surface.get_height())
        for name in self.names:
            # self.values[name] = True
            image = self.game.image.load("objects/images/lights/" + name + ".png")
            image = self.game.transform.scale(image, (self.square, self.square))
            self.lights[name] = image
    
    def update(self):
        pass

    def draw(self):
        self.surface.fill(0)
        i = 0
        j = 0
        for name in self.names:
            if self.values[name]:
                self.surface.blit(self.lights[name], (i*self.square, j*self.square))
            if i == 4:
                i = 0
                j += 1
            else:
                i += 1
        
        self.game.draw.rect(self.surface, (122,122,122), self.frame, 3)
        super().draw()

        
        


    