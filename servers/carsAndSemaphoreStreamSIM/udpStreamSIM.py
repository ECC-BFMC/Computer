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

        for x in range(semaphores):
            state, secs = random.choice(list(self.semaphore_pattern.items()))
            self.semaphore_state.append(state)
            self.semaphore_time.append(nowtime)
            self.semaphore_pos.append([x_y, x_y])
            x_y += 1

        # cars generation
        self.path = [
            (0.83, 14.67),
            (0.82, 14.29),
            (1.38, 13.73),
            (1.76, 13.74),
            (2.12, 13.73),
            (3.05, 12.08),
            (3.05, 12.42),
            (3.05, 12.04),
            (3.05, 11.66),
            (3.05, 11.41),
            (2.1, 10.47),
            (1.72, 10.47),
            (1.38, 10.46),
            (0.45, 11.39),
            (0.46, 11.77),
            (0.46, 12.15),
            (0.45, 12.52),
            (0.45, 12.8),
            (0.45, 14.29),
            (0.46, 14.67),
        ]
        cars = 1
        self.cars_pos = []

        for x in range(cars):
            self.cars_pos.append(random.randint(0, len(self.path)))

    def startProtocol(self):
        self.transport.setBroadcastAllowed(True)
        self.streaming_task = task.LoopingCall(self.send_message)
        self.streaming_task.start(self.frequency)

    def send_message(self):
        print("\033c")
        print("Status: ON")
        print("-------------------------------------------")
        print("No of Semaphores: ", len(self.semaphore_state))

        nowtime = time.time()
        for x in range(len(self.semaphore_state)):
            timepassed = nowtime - self.semaphore_time[x]
            if timepassed > self.semaphore_pattern[self.semaphore_state[x]]:
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
        print("No of Cars: ", len(self.cars_pos))
        for x in range(len(self.cars_pos)):
            tmp = self.cars_pos[x] + 1
            if tmp >= len(self.path):
                tmp = 0
            self.cars_pos[x] = tmp
            self.sendPos(x, self.path[tmp][0], self.path[tmp][1])
            print(
                "Car with id ", x, ", x=", self.path[tmp][0], ", y=", self.path[tmp][1]
            )

        print("To quit, press Ctrl+C")
        time.sleep(1)

    def stoptask(self):
        self.streaming_task.stop()  # Stop streaming when the server is stopped

    def sendState(self, id, state, x, y):
        value = {"device": "semaphore", "id": id, "state": state, "x": x, "y": y}
        message = json.dumps(value)
        self.transport.write(message.encode("utf-8"), self.address)

    def sendPos(self, id, x, y):
        value = {"device": "car", "id": id, "x": x, "y": y}
        message = json.dumps(value)
        self.transport.write(message.encode("utf-8"), self.address)


if __name__ == "__main__":
    streamport = 5007
    udp_factory = udpStream(streamport)

    reactor.listenUDP(streamport, udp_factory)

    reactor.run()

    udp_factory.stoptask()
