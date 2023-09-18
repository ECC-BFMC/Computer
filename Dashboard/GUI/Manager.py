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

# the State Manager is responsible for the state interraction
# this class represents the first layer of communication between the GUI_main class and the rest of the program
from GUI.DashBoard import DashBoard
from CarCommunication.threadwithstop import ThreadWithStop


class Manager(ThreadWithStop):
    clicked = False
    exit = False
    car_paired = False

    up = False
    down = False
    right = False
    left = False

    main_menu = False

    switching = False
    curtain_radius = 0
    curtain_state = 0
    curtain_speed = 10

    next_state = None

    def __init__(self, state, game, window):
        self.game = game
        self.window = window
        # this is the way te Manager will know which state to initialize
        self.state = DashBoard(game, window, self)

    # the update method calls the current state's update method
    # this method also updates the curtain if there is a change of state
    def update(self):
        self.state.update()

    # the draw method calls upon the current state's method
    # this method also draws the curtain if the state has been switched
    def draw(self):
        self.state.draw()
