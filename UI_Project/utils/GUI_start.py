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
from states.DashBoard import DashBoard
from utils.threadwithstop import ThreadWithStop
class threadGUI_start(ThreadWithStop):
    def __init__(self, pipeRecv, pipeSend):
        super(threadGUI_start,self).__init__()
        self.pipeSend = pipeSend
        self.pipeRecv = pipeRecv
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()

        # setting the window size 
        size = window_width, window_height = 800, 600
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)

        # setting the window caption 
        pygame.display.set_caption('BFMC Graphical Debugger')

        # initializing the current state, using the State Manager
        dashBoard = DashBoard(pygame, screen, self.pipeRecv, self.pipeSend)
        running = True

        while running:
            # setting a framerate of 60 fps
            clock.tick(60)
            # checking for all the input events that can happen (or other events can be checked here)
            # each frame has to be updated and redrawn accordingly 
            # every object in the program has an update method, a draw method and also an input method
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dashBoard.clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    dashBoard.clicked = False


            dashBoard.update()
            dashBoard.draw()
            pygame.display.update()
        pygame.quit()

    def stop(self):
        super(threadGUI_start,self).stop()


