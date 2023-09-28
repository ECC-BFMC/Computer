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


# Main function of the User Interface, where the first state is initialized
# The interface uses pygame, a library primarily created for games
import pygame
from GUI.DashBoard import DashBoard
from CarCommunication.threadwithstop import ThreadWithStop


class threadGUI_start(ThreadWithStop):
    """
    Initialize a threadGUI_start object.

    Args:
        pipeRecv (multiprocessing.Pipe): The pipe for receiving data in the GUI thread.
        pipeSend (multiprocessing.Pipe): The pipe for sending data from the GUI thread.
    """

    def __init__(self, pipeRecv, pipeSend):
        super(threadGUI_start, self).__init__()
        self.pipeSend = pipeSend
        self.pipeRecv = pipeRecv
        pygame.init()

    def run(self):
        """
        Run the graphical interface thread.

        This method initializes the graphical interface, handles user input events, updates
        the interface components, and manages the display loop.
        """
        clock = pygame.time.Clock()
        # setting the window size
        size = window_width, window_height = 1260, 500
        screen = pygame.display.set_mode(size)
        last_1_sec_call_time = pygame.time.get_ticks()
        last_60_fps_call_time = pygame.time.get_ticks()
        # setting the window caption
        pygame.display.set_caption("BFMC Graphical Interface")

        # initializing the current state, using the State Manager
        dashBoard = DashBoard(pygame, screen, self.pipeRecv, self.pipeSend)
        running = True
        i = 0
        while running:
            current_time = pygame.time.get_ticks()
            # checking for all the input events that can happen (or other events can be checked here)
            # each frame has to be updated and redrawn accordingly
            # every object in the program has an update method, a draw method and also an input method
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dashBoard.clicked = True
                elif event.type == pygame.MOUSEMOTION:
                    if dashBoard.clicked:
                        mouse_pos = pygame.mouse.get_pos()
                        dashBoard.table.update_checkbox(mouse_pos)
                        dashBoard.table.scrollSlider.colliding(mouse_pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    dashBoard.clicked = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    dashBoard.table.update_checkbox(mouse_pos)
                    if dashBoard.buttonAutonomEnable:
                        if dashBoard.button.colliding(mouse_pos):
                            dashBoard.button.update()
                            dashBoard.buttonSpeedEnable = (
                                not dashBoard.buttonSpeedEnable
                            )
                    if dashBoard.buttonSpeedEnable:
                        if dashBoard.button2.colliding(mouse_pos):
                            dashBoard.button2.update()
                            dashBoard.buttonAutonomEnable = (
                                not dashBoard.buttonAutonomEnable
                            )
                    if dashBoard.buttonSave.colliding(mouse_pos):
                        dashBoard.table.update_json()
                        dashBoard.set_text("save")
                    if dashBoard.buttonReset.colliding(mouse_pos):
                        dashBoard.table.reset_json()
                        dashBoard.set_text("reset")
                    if dashBoard.buttonLoad.colliding(mouse_pos):
                        dashBoard.table.load()
                        dashBoard.set_text("load")
                elif event.type == pygame.MOUSEWHEEL:
                    mouse_pos = pygame.mouse.get_pos()
                    dashBoard.table.scrollSlider.mouseWheelInteract(mouse_pos, event.y)
            if current_time - last_1_sec_call_time >= 50:  # 1000 ms = 1 second
                dashBoard.alerts.update(0.05)
                dashBoard.updateTimers(0.05)
                last_1_sec_call_time = current_time
            if current_time - last_60_fps_call_time >= 16:
                dashBoard.update()
                dashBoard.draw()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

    def stop(self):
        super(threadGUI_start, self).stop()
