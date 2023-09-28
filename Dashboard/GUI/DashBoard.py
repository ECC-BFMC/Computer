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

from GUI.State import State
from objects.Map import Map
from objects.Alerts import Alerts
from objects.Button import Button
from objects.Button_Text import Button_Text
from objects.Table import Table
from objects.Camera import Camera
from math import pi


class DashBoard(State):
    """
    Initialize a new instance of the class with various attributes.

    Args:
        game: The game object.
        window: The window object.
        pipeRecv (multiprocessing.Pipe): The pipe for receiving data.
        pipeSend (multiprocessing.Pipe): The pipe for sending data.
        speed (int, optional): The initial speed (default is 0).
        position (tuple, optional): The initial position (default is (0, 0)).
        battery (int, optional): The initial battery level (default is 100).
        lane_error (int, optional): The initial lane error (default is 0).
        steer (int, optional): The initial steering value (default is 0).

    """

    angle_change = 2
    steer_change = error_change = battery_dx = 1
    clicked = False

    def __init__(
        self,
        game,
        window,
        pipeRecv,
        pipeSend,
        speed=0,
        position=(0, 0),
        battery=100,
        lane_error=0,
        steer=0,
    ):
        super().__init__(game, window)
        self.pipeRecv = pipeRecv
        self.pipeSend = pipeSend
        self.battery = battery
        self.lane_error = lane_error
        self.list = [1, 20, 33, 55, 66]
        self.cursor_image = self.game.image.load("setup/images/cursor.png")
        self.cursor_image = self.game.transform.scale(self.cursor_image, (25, 110))
        self.cursor_pivot = (12, 12)
        self.angle = 0
        self.sem = True
        self.names = {"load": 0, "save": 0, "reset": 0}
        self.speed_image = self.game.image.load("setup/images/Speed_Meter.png")
        self.speed_image = self.game.transform.scale(self.speed_image, (300, 400))
        self.battery_color = (0, 255, 0)
        self.seconds_fadeaway = 3

        self.little_car = self.game.image.load("setup/images/little_car.png")
        self.little_car = self.game.transform.scale(self.little_car, (85, 132))

        self.steer = steer
        self.wheel = self.game.image.load("setup/images/wheel.png")
        self.wheel = self.game.transform.scale(self.wheel, (60, 60))
        self.wheel_pivot = (self.wheel.get_width() / 2, self.wheel.get_height() / 2)

        self.arrow = self.game.image.load("setup/images/arrow.png")
        self.arrow = self.game.transform.scale(self.arrow, (60, 60))
        self.arrow_pivot = (self.arrow.get_width() / 2, self.arrow.get_height() / 2)

        self.font_big = self.game.font.SysFont(None, 70)
        self.font_small = self.game.font.SysFont(None, 30)
        self.font_little = self.game.font.SysFont(None, 25)
        self.buttonAutonomEnable = True
        self.buttonSpeedEnable = True
        self.button = Button(
            500, 350, self.pipeSend, self.game, self.main_surface, "autonom"
        )
        self.button2 = Button(
            650, 350, self.pipeSend, self.game, self.main_surface, "speed"
        )
        self.map = Map(40, 30, self.game, self.main_surface, car_x=230, car_y=1920)
        self.alerts = Alerts(20, 240, self.game, self.main_surface, 250)
        self.table = Table(
            self.pipeSend,
            self.pipeRecv,
            550,
            10,
            self.game,
            self.main_surface,
            width=600,
            height=300,
        )
        self.camera = Camera(850, 350, self.game, self.main_surface)
        self.buttonSave = Button_Text(970, 315, self.game, self.main_surface, "Save")
        self.buttonLoad = Button_Text(1045, 315, self.game, self.main_surface, "Load")
        self.buttonReset = Button_Text(1120, 315, self.game, self.main_surface, "Reset")
        self.objects = [self.map, self.alerts, self.table, self.camera]

    def blitRotate(self, surf, image, pos, originPos, angle):
        """
        Rotate an image and blit it onto a surface.

        Args:
            surf: The target surface where the rotated image will be blitted.
            image: The image to be rotated and blitted.
            pos (tuple): The position (x, y) where the rotated image will be blitted.
            originPos (tuple): The pivot point (x, y) around which the image will be rotated.
            angle (float): The angle in degrees by which the image will be rotated.
        """
        image_rect = image.get_rect(
            topleft=(pos[0] - originPos[0], pos[1] - originPos[1])
        )
        offset_center_to_pivot = self.game.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = self.game.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

    def continous_update(self):
        """
        Continuously update the class attributes based on received messages.

        This method listens for incoming messages on the `pipeRecv` pipe and updates
        the class attributes accordingly, depending on the message type.
        """
        if self.pipeRecv.poll():
            msg = self.pipeRecv.recv()
            if msg["action"] == "steering":
                self.steer = -1 * msg["value"]
            elif msg["action"] == "modImg":
                self.camera.change_frame(msg["value"])
            elif msg["action"] == "map":
                terms_list = msg["value"].split()
                x = float(terms_list[1][0 : len(terms_list[1]) - 1]) * 150
                y = float(terms_list[3][0 : len(terms_list[3]) - 1]) * 150
                self.map.new_coordinates(x, y)
                self.map.update()
            elif msg["action"] == "battery":
                self.battery = msg["value"]
            elif msg["action"] == "engStart":
                self.table.addValueFromPI("Able to start", msg["value"])
            elif msg["action"] == "engRunning":
                self.table.addValueFromPI("Engine running", msg["value"])
            elif msg["action"] == "speed":
                self.angle = self.rad_to_degrees(-1 * msg["value"])
            elif msg["action"] == "roadOffset":
                self.little_car = self.game.transform.scale(
                    self.little_car, (85 + msg["value"], 132)
                )
            elif msg["action"] == "emptyAll":
                self.camera.conn_lost()

    def updateTimers(self, timePassed):
        """
        Update timers associated with named actions.

        This method updates timers for named actions stored in the `names` dictionary.
        It subtracts the specified `timePassed` from the timers.

        Args:
            timePassed (float): The time passed, in seconds.
        """
        for key, value in self.names.items():
            self.names[key] = value - timePassed

    def set_text(self, text):
        """
        Set a timer for a named action.

        This method sets a timer for a named action specified by the `text` parameter.
        The timer is initially set to 3.0 seconds.

        Args:
            text (str): The name of the action.
        """
        self.names[text] = 3.0

    def update(self):
        """
        Update the class state.

        This method updates the class state by performing the following actions:
        1. Calls the superclass's update method using `super()`.
        2. Calls the `continous_update` method to process incoming messages and update attributes.
        3. Calls the `input` method to handle user input.
        4. Adjusts the `battery_color` attribute based on the current battery level.
        """
        super().update()
        self.continous_update()
        self.input()
        self.battery_color = (
            (100 - self.battery) * 255 / 100,
            (self.battery / 100) * 255,
            0,
        )

    def rad_to_degrees(self, angle):
        """
        Convert an angle from radians to degrees.

        Args:
            angle (float): The angle in radians to be converted.

        """
        converted = angle * 180 / pi
        return converted

    def deg_to_radians(self, angle):
        """
        Convert an angle from degrees to radians.

        Args:
            angle (float): The angle in degrees to be converted.

        """
        converted = angle * pi / 180
        return converted

    def draw(self):
        """
        Draw the graphical elements on the main surface.

        This method clears the main surface, draws operation success messages with fading,
        draws various objects, buttons, battery level, speed image, and the little car image.

        """
        self.main_surface.fill(0)
        for key, value in self.names.items():
            if value > 0:
                text_surface = self.font_small.render(
                    key + " operation successfully", True, (255, 255, 255)
                )
                text_surface.set_alpha(255 / self.seconds_fadeaway * value)
                self.main_surface.blit(text_surface, (550, 310))

        for object in self.objects:
            object.draw()
        if self.buttonAutonomEnable:
            self.button.draw()
        if self.buttonSpeedEnable:
            self.button2.draw()
        self.buttonSave.draw()
        self.buttonLoad.draw()
        self.buttonReset.draw()
        battery_show = self.font_small.render(
            str(self.battery) + "%", True, self.battery_color
        )
        self.main_surface.blit(battery_show, (280, 10))
        self.main_surface.blit(self.speed_image, (250, -25))

        self.game.draw.line(self.main_surface, (255, 255, 255), (330, 480), (330, 310))
        self.game.draw.line(self.main_surface, (255, 255, 255), (460, 480), (460, 310))
        self.main_surface.blit(self.little_car, (353 + self.lane_error, 350))
        self.game.draw.arc(
            self.main_surface,
            self.battery_color,
            [260, 10, 280, 250],
            pi / 4 + (100 - self.battery) * (pi / 2) / 100,
            pi - pi / 4,
            25,
        )

        self.blitRotate(
            self.main_surface,
            self.cursor_image,
            (400, 165),
            self.cursor_pivot,
            self.angle,
        )

        self.blitRotate(
            self.main_surface, self.arrow, (395, 320), self.arrow_pivot, 90 + self.steer
        )

        if -self.steer > 0:
            steer_show = self.font_little.render(
                "+" + str(-self.steer) + "°", True, (255, 255, 255)
            )
            self.main_surface.blit(steer_show, (425, 300))
        elif -self.steer <= 0:
            steer_show = self.font_little.render(
                str(-self.steer) + "°", True, (255, 255, 255)
            )
            self.main_surface.blit(steer_show, (337, 300))
        super().draw()
