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

# Module imports
import time
import json
import random

from twisted.internet import reactor
from twisted.internet import task, protocol


class udpStream(protocol.DatagramProtocol):
    def __init__(self, streamPort, frequency=0.1):
        # Initialize the udpStream object
        self.address = ("<broadcast>", streamPort)
        self.frequency = frequency

        # semaphores generation
        self.semaphore_pattern = {"green": 5, "yellow": 2, "red": 7}
        semaphores = 4
        self.semaphore_state = []
        self.semaphore_time = []
        self.semaphore_pos = []
        x_y = 1
        nowtime = time.time()

        # Generate semaphores with random states and positions
        for x in range(semaphores):
            state, secs = random.choice(list(self.semaphore_pattern.items()))
            self.semaphore_state.append(state)
            self.semaphore_time.append(nowtime)
            self.semaphore_pos.append([x_y, x_y])
            x_y += 1

    def startProtocol(self):
        # Set the protocol to allow broadcasting
        self.transport.setBroadcastAllowed(True)
        self.streaming_task = task.LoopingCall(self.send_message)
        self.streaming_task.start(self.frequency)

    def send_message(self):
        # Print the current status and number of semaphores
        print("\033c")
        print("Status: ON")
        print("-------------------------------------------")
        print("No of Semaphores: ", len(self.semaphore_state))

        nowtime = time.time()
        for x in range(len(self.semaphore_state)):
            timepassed = nowtime - self.semaphore_time[x]
            if timepassed > self.semaphore_pattern[self.semaphore_state[x]]:
                # Update the semaphore state based on the pattern
                self.semaphore_time[x] = nowtime
                if self.semaphore_state[x] == "red":
                    self.semaphore_state[x] = "green"
                elif self.semaphore_state[x] == "yellow":
                    self.semaphore_state[x] = "red"
                elif self.semaphore_state[x] == "green":
                    self.semaphore_state[x] = "yellow"
            self.sendState(
                x,
                self.semaphore_state[x],
                self.semaphore_pos[x][0],
                self.semaphore_pos[x][1],
            )
            # Print the state and position of each semaphore
            print(
                "Semaphore with id ",
                x,
                ", the state is: ",
                self.semaphore_state[x],
                ", x=",
                self.semaphore_pos[x][0],
                ", y=",
                self.semaphore_pos[x][1],
            )
        print("-------------------------------------------")
        print("To quit, press Ctrl+C")
        time.sleep(1)

    def stoptask(self):
        # Stop the streaming task when the server is stopped
        self.streaming_task.stop()

    def sendState(self, id, state, x, y):
        # Send the state of a semaphore to the specified address
        value = {"device": "semaphore", "id": id, "state": state, "x": x, "y": y}
        message = json.dumps(value)
        self.transport.write(message.encode("utf-8"), self.address)

    def sendPos(self, id, x, y):
        # Send the position of a car to the specified address
        value = {"device": "car", "id": id, "x": x, "y": y}
        message = json.dumps(value)
        self.transport.write(message.encode("utf-8"), self.address)


if __name__ == "__main__":
    streamport = 5007
    udp_factory = udpStream(streamport)

    # Start listening for UDP packets on the specified port
    reactor.listenUDP(streamport, udp_factory)

    # Start the Twisted reactor
    reactor.run()

    # Stop the streaming task
    udp_factory.stoptask()
