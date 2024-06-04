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

from twisted.internet import protocol, task
import json
import itertools
import re

def extract_positions_from_log(log_file_path):
    positions = []
    pattern = re.compile(r"'x': '([-+]?\d*\.\d+|\d+)', 'y': '([-+]?\d*\.\d+|\d+)', 'quality': (\d+)")
    
    with open(log_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                quality = int(match.group(3))
                positions.append((x, y, quality))
    return positions

class tcpServerLocsys(protocol.Factory):
    def __init__(self):
        self.path = extract_positions_from_log("servers/trafficCommunicationServer/Useful/sample_data.log")
        print(self.path)
        self.frequency = 0.2
        self.connections = {}

    def buildProtocol(self, addr):
        conn = SingleConnection()
        conn.factory = self
        return conn

class SingleConnection(protocol.Protocol):
    def connectionMade(self):
        peer = self.transport.getPeer()
        self.connectiondata = peer.host + ":" + str(peer.port)
        self.factory.connections[self.connectiondata] = self
        print(
            "Connection with :",
            self.connectiondata,
            " established for locsys device simulator",
        )
        self.array_iterator = itertools.cycle(self.factory.path)
        self.streaming_task = task.LoopingCall(self.send_data)
        self.streaming_task.start(self.factory.frequency)

    def connectionLost(self, reason):
        print(
            "Connection lost with ",
            self.connectiondata,
            " due to: ",
            reason,
            "for locsys device simulator",
        )
        del self.factory.connections[self.connectiondata]
        self.streaming_task.stop()

    def send_data(self):
        pos = next(self.array_iterator)
        tosend = {"x": pos[0], "y": pos[1], "quality": pos[2]}
        msgtosend = json.dumps(tosend)
        self.transport.write(msgtosend.encode())
