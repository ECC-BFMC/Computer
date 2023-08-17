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
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Table(Object):
    title = "Messages"
    found = False
    rows = []
    text_color = WHITE

    def __init__(self, pipeSend, pipeRecv, x, y, game, window, width=600, height=300):
        super().__init__(x, y, game, window, width, height)
        self.num_columns = 3
        self.width = width
        self.height = height
        self.pipeSend = pipeSend
        self.pipeRecv = pipeRecv
        self.x = x
        self.checked = []
        self.y = y
        self.rectangleCheckboxList = []
        self.rectangleValueLIst = []
        self.rectangleOptionList = []
        self.rectangleModiffiedList = []
        self.modifiedValues = []
        self.textOptionList = []
        self.column_width = [300, 200, 100]
        self.font = self.game.font.SysFont(None, 25)
        self.checkbox_size = 20
        self.checkbox_padding = 10
        self.data = {}
        self.data_raw = {}
        self.dataEnums = {}
        self.reset_json()
        self.showMenu = False
        self.valueToBeChanged = 0
        self.keyToBeChanged = ""

    def update(self):
        pass

    def load(self):
        if len(self.checked) > 0:
            for e in self.checked:
                key = self.get_dict_key(e, self.data)
                self.pipeSend.send({"action": key, "value": self.data[key]["defVal"]})

    def update_checkbox(self, mouse_pos):
        for e in range(len(self.rectangleCheckboxList)):
            if self.rectangleCheckboxList[e].collidepoint(mouse_pos):
                if e not in self.checked:
                    self.checked.append(e)
                else:
                    self.checked.remove(e)
        if self.showMenu == False:
            for e in range(len(self.rectangleValueLIst)):
                if self.rectangleValueLIst[e].collidepoint(mouse_pos):
                    self.showMenu = not self.showMenu
                    self.valueToBeChanged = e
                    self.keyToBeChanged = self.get_dict_key(e, self.dataEnums)
                    for i in range(len(self.dataEnums[self.keyToBeChanged]["vals"])):
                        rectangleDropdown = self.game.Rect(
                            self.column_width[0] + self.x + self.checkbox_padding,
                            self.checkbox_size * i
                            + 30 * e
                            + self.checkbox_padding
                            + self.y,
                            self.checkbox_size * 2 + 20,
                            self.checkbox_size,
                        )
                        self.rectangleOptionList.append(rectangleDropdown)
                        self.textOptionList.append(
                            (
                                self.column_width[0] + self.x + self.checkbox_padding,
                                self.checkbox_size * i
                                + 30 * e
                                + self.checkbox_padding
                                + self.y,
                            )
                        )
        else:
            for e in range(len(self.rectangleOptionList)):
                if self.rectangleOptionList[e].collidepoint(mouse_pos):
                    self.dataEnums[self.keyToBeChanged]["defVal"] = self.dataEnums[
                        self.keyToBeChanged
                    ]["vals"][e]
            self.rectangleOptionList = []
            self.textOptionList = []
            self.showMenu = False
        self.verify_values()

    def saveValues(self):
        for key, value in self.values.items():
            if key in self.saved_values_mod.keys():
                self.saved_values_mod[key] = value

    def verify_values(self):
        self.modifiedValues = []
        for key, value in self.dataEnums.items():
            if self.data_raw[key]["defVal"] != value["defVal"]:
                self.modifiedValues.append(self.get_dict_number(key, self.dataEnums))
        self.create_modified_rectangles()

    def draw(self):
        for e in self.rectangleCheckboxList:
            self.game.draw.rect(self.window, WHITE, e, 1)
        for e in self.checked:
            self.game.draw.rect(
                self.window, WHITE, self.rectangleCheckboxList[e].inflate(-8, -8)
            )
        for e in self.rectangleValueLIst:
            self.game.draw.rect(self.window, WHITE, e, 1)
        for e in self.rectangleModiffiedList:
            self.game.draw.rect(self.window, RED, e.inflate(0, 0))
        if self.found:
            self.surface.blit(self.image, (10, 30))
        sumwidth = 0
        for col in range(self.num_columns):
            if col < 2:
                column_rect = self.game.Rect(
                    sumwidth + self.x, self.y, self.column_width[col], self.height
                )
            else:
                column_rect = self.game.Rect(
                    sumwidth + self.x, self.y, 2 * self.checkbox_size, self.height
                )
            self.game.draw.rect(self.window, RED, column_rect, 1)
            sumwidth += self.column_width[col]
            if col == 0:
                for index, e in enumerate(self.dataEnums.keys()):
                    text_surface = self.font.render(e, True, WHITE)
                    text_x = self.x + 10
                    text_y = self.y + 30 * index + 10
                    index += 1
                    self.window.blit(text_surface, (text_x, text_y))
            elif col == 1:
                for index, e in enumerate(self.dataEnums.values()):
                    text_surface = self.font.render(e["defVal"], True, WHITE)
                    text_x = self.x + 10 + self.column_width[0]
                    text_y = self.y + 30 * index + 10
                    self.window.blit(text_surface, (text_x, text_y))
        if self.showMenu:
            for e in self.rectangleOptionList:
                self.game.draw.rect(self.window, WHITE, e.inflate(0, 0))
            for e in range(len(self.dataEnums[self.keyToBeChanged]["vals"])):
                self.window.blit(
                    self.font.render(
                        self.dataEnums[self.keyToBeChanged]["vals"][e], True, BLACK
                    ),
                    self.textOptionList[e],
                )
            borderRectangleX = self.column_width[0] + self.x + 5
            borderRectangleY = (
                self.y + 5 + (self.checkbox_size + 10) * self.valueToBeChanged
            )
            borderRectangleWidth = self.checkbox_size * 2 + 30
            borderRectangleHeight = (
                self.checkbox_size * len(self.dataEnums[self.keyToBeChanged]["vals"])
                + 10
            )
            borderRectangle = self.game.Rect(
                borderRectangleX,
                borderRectangleY,
                borderRectangleWidth,
                borderRectangleHeight,
            )
            self.game.draw.rect(self.window, WHITE, borderRectangle, 1)

    def create_rectangles(self):
        for i, e in enumerate(self.dataEnums.keys()):
            rectangleCheckboxe = self.game.Rect(
                self.column_width[0]
                + self.column_width[1]
                + self.checkbox_padding
                + self.x,
                30 * i + self.checkbox_padding + self.y,
                self.checkbox_size,
                self.checkbox_size,
            )
            rectangleDropdown = self.game.Rect(
                self.column_width[0] + self.x + self.checkbox_padding,
                30 * i + self.checkbox_padding + self.y,
                self.checkbox_size * 2 + 20,
                self.checkbox_size,
            )
            self.rectangleCheckboxList.append(rectangleCheckboxe)
            self.rectangleValueLIst.append(rectangleDropdown)

    def create_modified_rectangles(self):
        for e in self.modifiedValues:
            rectangleModfieid = self.game.Rect(
                self.column_width[0] + self.column_width[1] - 30 + self.x,
                30 * e + self.checkbox_padding + self.y,
                self.checkbox_size,
                self.checkbox_size,
            )
            self.rectangleModiffiedList.append(rectangleModfieid)

    def update_json(self):
        self.modifiedValues = []
        self.rectangleModiffiedList = []
        self.data.update(self.dataEnums)
        with open("utils/CarData.json", "w") as f:
            json.dump(self.data, f, indent=4)

    def get_dict_key(self, number, dictionary):
        for index, key in enumerate(dictionary.keys()):
            if index == number:
                return key

    def get_dict_number(self, key, dictionary):
        for index, keyDict in enumerate(dictionary.keys()):
            if keyDict == key:
                return index

    def reset_json(self):
        with open("utils/CarData.json", "r") as f:
            self.data_raw = json.load(f)
            self.data = copy.deepcopy(self.data_raw)
        for key, value in self.data.items():
            if value["type"] == "enum":
                self.dataEnums[key] = value
        self.rectangleValueLIst = []
        self.rectangleCheckboxList = []
        self.rectangleOptionList = []
        self.modifiedValues = []
        self.rectangleModiffiedList = []
        self.create_rectangles()
