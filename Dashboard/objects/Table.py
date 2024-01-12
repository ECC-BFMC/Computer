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
from objects.Slider import Slider
from objects.ScrollSlider import ScrollSlider
import json
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Table(Object):
    """
    Initialize a table for displaying data with checkboxes and sliders.

    Args:
        pipeSend: The pipe for sending data.
        pipeRecv: The pipe for receiving data.
        x (int): The x-coordinate of the table.
        y (int): The y-coordinate of the table.
        game: The game object.
        window: The window object.
        width (int, optional): The width of the table (default is 740).
        height (int, optional): The height of the table (default is 300).

    """

    title = "Messages"
    found = False
    rows = []
    text_color = WHITE

    def __init__(self, pipeSend, pipeRecv, x, y, game, window, width=740, height=300):
        super().__init__(x, y, game, window, width, height)
        self.num_columns = 4
        self.width = width
        self.height = height
        self.pipeSend = pipeSend
        self.pipeRecv = pipeRecv
        self.x = x
        self.checked = []
        self.y = y
        self.minScroll = 0
        self.last_minScroll = 1
        self.maxScroll = 9
        self.startEnums = 0
        self.stopEnums = 0
        self.startRange = 0
        self.stopRange = 0
        self.startFromPI = 0
        self.stopFromPI = 0
        self.rectangleCheckboxList = []
        self.valuesFromPi = {}
        self.rectangleValueLIst = []
        self.rectangleOptionList = []
        self.rectangleModiffiedList = []
        self.modifiedValues = []
        self.textOptionList = []
        self.column_width = [300, 300, 40, 15]
        self.font = self.game.font.SysFont(None, 25)
        self.font_small = self.game.font.SysFont(None, 18)
        self.checkbox_size = 20
        self.checkbox_padding = 10
        self.data = {}
        self.data_raw = {}
        self.dataEnums = {}
        self.dataRange = {}
        self.sliders = []
        self.scrollSlider = ScrollSlider(
            self.x + self.width + 25,
            self.y,
            len(self.rectangleCheckboxList) + len(self.valuesFromPi),
            self.game,
            self.window,
            width=15,
            height=self.height,
        )
        self.reset_json()
        self.showMenu = False
        self.valueToBeChanged = 0
        self.keyToBeChanged = ""

    def update(self):
        """
        Update the table's state and scroll slider.
        """
        self.scrollSlider.update()

    def addValueFromPI(self, key, value):
        """
        Add a value received from the Raspberry Pi to the table.

        Args:
            key (str): The key associated with the value.
            value: The value received from the Raspberry Pi.
        """
        self.valuesFromPi[key] = value

    def load(self):
        """
        Load values from the GUI to the Raspberry Pi.

        This method sends the selected values from the GUI to the Raspberry Pi for loading.

        Note:
            It sends either default enum values or slider values based on the selected checkboxes.

        """
        if len(self.checked) > 0:
            for e in self.checked:
                key = self.get_dict_key(e, self.data)
                if e < len(self.dataEnums):
                    self.pipeSend.send(
                        {"action": key, "value": self.dataEnums[key]["defVal"]}
                    )
                else:
                    self.pipeSend.send(
                        {
                            "action": key,
                            "value": self.sliders[e - len(self.dataEnums)].defValue,
                        }
                    )

    def redo_sliders(self):
        """
        Redo the sliders in the GUI based on data range specifications.

        This method recreates the slider objects in the GUI based on the data range specifications.

        Note:
            It clears the existing sliders and creates new ones according to the data range.

        """
        self.sliders = []
        for index, e in enumerate(self.dataRange.keys()):
            slider = Slider(
                self.column_width[0]
                + self.checkbox_padding
                + self.x
                + self.checkbox_size * 3,
                30 * (index + len(self.dataEnums)) + self.y + 5,
                self.dataRange[e]["precision"],
                self.dataRange[e]["defVal"],
                self.dataRange[e]["min"],
                self.dataRange[e]["max"],
                self.game,
                self.window,
                101,
                10,
            )
            self.sliders.append(slider)

    def update_checkbox(self, mouse_pos):
        """
        Update checkbox interactions in the GUI.

        This method handles interactions with checkboxes, sliders, and dropdown menus based on mouse positions.

        Args:
            mouse_pos (tuple): The mouse cursor's position (x, y).

        """
        for e in range(len(self.rectangleCheckboxList)):
            if self.rectangleCheckboxList[e].collidepoint(mouse_pos):
                if e not in self.checked:
                    self.checked.append(e)
                else:
                    self.checked.remove(e)
        if self.showMenu == False:
            for e in self.sliders:
                e.colliding(mouse_pos)
            for e in range(len(self.rectangleValueLIst)):
                if self.startEnums >= 0:
                    if self.rectangleValueLIst[e - self.startEnums].collidepoint(
                        mouse_pos
                    ):
                        self.showMenu = not self.showMenu
                        self.keyToBeChanged = self.get_dict_key(e, self.dataEnums)
                        for i in range(
                            len(self.dataEnums[self.keyToBeChanged]["vals"])
                        ):
                            rectangleDropdown = self.game.Rect(
                                self.column_width[0]
                                + self.x
                                + self.checkbox_padding
                                + 100,
                                self.checkbox_size * i
                                + 30 * (self.valueToBeChanged)
                                + self.checkbox_padding
                                + self.y,
                                self.checkbox_size * 2 + 20,
                                self.checkbox_size,
                            )
                            self.rectangleOptionList.append(rectangleDropdown)
                            self.textOptionList.append(
                                (
                                    self.column_width[0]
                                    + self.x
                                    + self.checkbox_padding
                                    + 100,
                                    self.checkbox_size * i
                                    + 30 * (self.valueToBeChanged)
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
        """
        Save modified values to the saved_values_mod dictionary.

        This method iterates through the current values and updates the corresponding values in the saved_values_mod dictionary.

        """
        for key, value in self.values.items():
            if key in self.saved_values_mod.keys():
                self.saved_values_mod[key] = value

    def verify_values(self):
        """
        Verify and track modified values.

        This method checks if any values in the data dictionaries (dataEnums and dataRange) have been modified and
        updates the modifiedValues list accordingly. It also creates rectangles for visualizing modified values.

        """
        self.modifiedValues = []
        self.rectangleModiffiedList = []
        for key, value in self.dataEnums.items():
            if self.data_raw[key]["defVal"] != value["defVal"]:
                self.modifiedValues.append(self.get_dict_number(key, self.dataEnums))
        for index, slider in enumerate(self.sliders):
            key = self.get_dict_key(index, self.dataRange)
            if float(self.data_raw[key]["defVal"]) != slider.defValue:
                self.modifiedValues.append(index + len(self.dataEnums))
        self.create_modified_rectangles()

    def draw(self):
        """
        Draw the interface elements on the window.

        This method visually renders checkboxes, modified values, enums, sliders, values from Pi, columns,
        and dropdown menus (if shown).

        """
        if self.minScroll != self.last_minScroll:
            self.last_minScroll = self.minScroll
            self.redo_sliders()
        self.scrollSlider.maximum = (
            len(self.dataEnums) + len(self.dataRange) + len(self.valuesFromPi)
        )
        self.update()
        self.scrollSlider.draw()
        self.minScroll = +6 + len(self.dataRange) - self.scrollSlider.current_value
        self.maxScroll = (
            len(self.dataEnums)
            + len(self.dataRange)
            - self.scrollSlider.current_value
            + (self.scrollSlider.pin_range_end - self.scrollSlider.pin_range_start)
        )
        if self.minScroll <= len(self.dataEnums):
            self.startEnums = self.minScroll
        else:
            self.startEnums = -1
        if self.maxScroll <= len(self.dataEnums):
            self.stopEnums = self.maxScroll
        else:
            self.stopEnums = len(self.dataEnums)
        if len(self.dataEnums) < self.maxScroll:
            self.startRange = (
                self.minScroll
                - self.maxScroll
                + len(self.dataEnums)
                + len(self.dataRange)
            )
        else:
            self.startRange = -1
        if len(self.dataRange) >= self.maxScroll - len(self.dataEnums) + 1:
            self.stopRange = self.maxScroll - len(self.dataEnums) + 1
        else:
            self.stopRange = len(self.dataRange)
        if len(self.dataEnums) + len(self.dataRange) <= self.maxScroll:
            self.stopFromPI = self.maxScroll - (
                len(self.dataEnums) + len(self.dataRange)
            )
            if self.minScroll <= len(self.valuesFromPi) + 1:
                self.startFromPI = self.minScroll
            else:
                self.startFromPI = 0
        else:
            self.stopFromPI = -1
        #############################################################
        # checkboxes
        for e in self.rectangleCheckboxList:
            self.game.draw.rect(self.window, WHITE, e, 1)
        for e in self.checked:
            self.game.draw.rect(
                self.window, WHITE, self.rectangleCheckboxList[e].inflate(-8, -8)
            )
        #############################################################
        # modified
        for e in self.rectangleModiffiedList:
            self.game.draw.rect(self.window, RED, e.inflate(0, 0))
        #############################################################
        # ENUMS
        for index, e in enumerate(self.dataEnums.keys()):
            if (
                index >= self.startEnums
                and self.startEnums >= 0
                and index <= self.stopEnums
            ):
                text_surface = self.font.render(e, True, WHITE)
                text_x = self.x + 10
                text_y = self.y + 30 * (index - self.startEnums) + 10
                self.window.blit(text_surface, (text_x, text_y))
                rectangleDropdown = self.game.Rect(
                    self.column_width[0] + self.x + self.checkbox_padding,
                    30 * (index - self.startEnums) + self.checkbox_padding + self.y,
                    self.checkbox_size * 2 + 20,
                    self.checkbox_size,
                )
                self.game.draw.rect(self.window, WHITE, rectangleDropdown, 1)
        for index, e in enumerate(self.dataEnums.values()):
            if (
                index >= self.startEnums
                and self.startEnums >= 0
                and index <= self.stopEnums
            ):
                text_surface = self.font.render(e["defVal"], True, WHITE)
                text_x = self.x + 10 + self.column_width[0]
                text_y = self.y + 30 * (index - self.startEnums) + 10
                self.window.blit(text_surface, (text_x, text_y))
        #############################################################
        # sliders
        for index, slider in enumerate(self.sliders):
            if index < self.stopRange and self.startRange >= 0:
                slider.draw()
                text_surface = self.font.render(
                    "Val: " + str(slider.defValue), True, WHITE
                )
                text_x = slider.slider_x + 45 + slider.width
                text_y = slider.slider_y - 3
                self.window.blit(text_surface, (text_x, text_y))
                text_surface_min = self.font_small.render(
                    "(" + str(slider.minimum) + ")", True, WHITE
                )
                text_x = slider.slider_x - 30
                text_y = slider.slider_y
                self.window.blit(text_surface_min, (text_x, text_y))
                text_surface_max = self.font_small.render(
                    "(" + str(slider.maximum) + ")", True, WHITE
                )
                text_x = slider.slider_x + slider.slider_width + 5
                text_y = slider.slider_y
                self.window.blit(text_surface_max, (text_x, text_y))
        for index, e in enumerate(self.dataRange.keys()):
            if index < self.stopRange and self.startRange >= 0:
                text_surface = self.font.render(e, True, WHITE)
                text_x = self.x + 10
                text_y = (
                    self.y
                    + 30 * (index - self.maxScroll + self.stopEnums + 2)
                    + 10
                    + len(self.dataEnums) * 30
                )
                self.window.blit(text_surface, (text_x, text_y))
        #############################################################
        # vals from pi
        for index, e in enumerate(self.valuesFromPi.keys()):
            if self.stopFromPI >= 0 and index >= self.startFromPI:
                text_surface = self.font.render(e, True, WHITE)
                text_x = self.x + 10
                text_y = (
                    self.y + 30 * (index + self.stopRange + len(self.dataEnums)) + 10
                )
                self.window.blit(text_surface, (text_x, text_y))
        for index, e in enumerate(self.valuesFromPi.values()):
            if self.stopFromPI >= 0 and index >= self.startFromPI:
                text_surface = self.font.render(e, True, WHITE)
                text_x = self.x + 10 + self.column_width[0]
                text_y = (
                    self.y + 30 * (index + self.stopRange + len(self.dataEnums)) + 10
                )
                self.window.blit(text_surface, (text_x, text_y))
        #############################################################
        # cols
        sumwidth = 0
        for col in range(self.num_columns):
            column_rect = self.game.Rect(
                sumwidth + self.x, self.y, self.column_width[col], self.height
            )
            self.game.draw.rect(self.window, RED, column_rect, 1)
            sumwidth += self.column_width[col]
        #############################################################
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
            borderRectangleX = self.column_width[0] + self.x + 105
            borderRectangleY = (
                self.y + 5 + (self.checkbox_size + 10) * (self.valueToBeChanged)
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
        """
        Create and initialize rectangles for checkboxes and dropdown menus.

        This method initializes two lists:
        - `self.rectangleCheckboxList`: Stores rectangles for checkboxes.
        - `self.rectangleValueList`: Stores rectangles for dropdown menus (associated with enum elements).

        """
        self.rectangleCheckboxList = []
        self.rectangleValueLIst = []
        for index, e in enumerate(self.dataEnums.keys()):
            rectangleCheckboxe = self.game.Rect(
                self.column_width[0]
                + self.column_width[1]
                + self.checkbox_padding
                + self.x,
                30 * (index - self.startEnums) + self.checkbox_padding + self.y,
                self.checkbox_size,
                self.checkbox_size,
            )
            if index >= self.startEnums and self.startEnums >= 0:
                rectangleDropdown = self.game.Rect(
                    self.column_width[0] + self.x + self.checkbox_padding,
                    30 * (index - self.startEnums) + self.checkbox_padding + self.y,
                    self.checkbox_size * 2 + 20,
                    self.checkbox_size,
                )
                self.rectangleValueLIst.append(rectangleDropdown)
            self.rectangleCheckboxList.append(rectangleCheckboxe)
        for i, e in enumerate(self.dataRange.keys()):
            rectangleCheckboxe = self.game.Rect(
                self.column_width[0]
                + self.column_width[1]
                + self.checkbox_padding
                + self.x,
                30 * i + self.checkbox_padding + self.y + (1 + index) * 30,
                self.checkbox_size,
                self.checkbox_size,
            )
            self.rectangleCheckboxList.append(rectangleCheckboxe)

    def create_modified_rectangles(self):
        """
        Create and initialize rectangles to highlight modified values.

        This method creates rectangles around elements that have been modified
        to visually indicate changes in the interface.

        """
        for e in self.modifiedValues:
            rectangleModfieid = self.game.Rect(
                self.column_width[0] + self.column_width[1] - 30 + self.x,
                30 * e + self.checkbox_padding + self.y,
                self.checkbox_size,
                self.checkbox_size,
            )
            self.rectangleModiffiedList.append(rectangleModfieid)

    def update_json(self):
        """
        Update and save the JSON data representing the interface state.

        This method combines data from different sources, updates the JSON file,
        and then resets the JSON data to its original state.

        """
        self.modifiedValues = []
        self.rectangleModiffiedList = []
        self.data.update(self.dataEnums)
        for index, e in enumerate(self.sliders):
            self.dataRange[self.get_dict_key(index, self.dataRange)][
                "defVal"
            ] = e.defValue
        self.data.update(self.dataRange)
        with open("utils/CarData.json", "w") as f:
            json.dump(self.data, f, indent=4)
        self.reset_json()

    def get_dict_key(self, number, dictionary):
        """
        Get the key from a dictionary based on its position (index) in the dictionary.

        Args:
            number (int): The index of the key to retrieve.
            dictionary (dict): The dictionary to extract the key from.

        Returns:
            str: The key corresponding to the specified index in the dictionary.

        """
        for index, key in enumerate(dictionary.keys()):
            if index == number:
                return key

    def get_dict_number(self, key, dictionary):
        """
        Get the index (position) of a key within a dictionary.

        Args:
            key (str): The key to find the index of.
            dictionary (dict): The dictionary to search for the key.

        Returns:
            int: The index of the key within the dictionary.

        """
        for index, keyDict in enumerate(dictionary.keys()):
            if keyDict == key:
                return index

    def reset_json(self):
        """
        Reset attributes and load data from a JSON file.

        Resets various attributes to their initial values, loads data from a JSON file,
        categorizes the data into dictionaries based on their "type" key, and prepares
        rectangles for display.

        """
        self.minScroll = 0
        self.maxScroll = 9
        self.startEnums = 0
        with open("setup/CarData.json", "r") as f:
            self.data_raw = json.load(f)
            self.data = copy.deepcopy(self.data_raw)
        for key, value in self.data.items():
            if value["type"] == "enum":
                self.dataEnums[key] = value
            else:
                self.dataRange[key] = value
        self.rectangleValueLIst = []
        self.rectangleCheckboxList = []
        self.rectangleOptionList = []
        self.modifiedValues = []
        self.rectangleModiffiedList = []
        self.redo_sliders()
        self.valuesFromPi = {}
        self.create_rectangles()
