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

from Useful.fileHandler import FileHandler

import threading
from collections import deque
from copy import deepcopy
import json


class dataDealer:
    def __init__(self):
        self.lock = threading.Lock()
        self.alldata = {}
        self.connected = []
        self.fileHandler = FileHandler("historyFile.txt")
        data_points = deque(
            maxlen=30
        )  # Creates and handles a list of maximum n points. discarding old ones when appending new data.
        self.carDataSample = {
            "devicePos": (0.0, 0.0),
            "deviceRot": 0.0,
            "deviceSpeed": 0.0,
            "historyData": data_points,
        }

        self.devices = {
            1: "192.168.1.31:4691",
            2: "192.168.1.32:4691",
            3: "192.168.88.11:4691",
            4: "192.168.1.34:4691",
        }

        self.teams = {
            "192.168.1.61": "Popa",
            "192.168.1.62": "Lopa",
            "192.168.1.63": "Mopa",
            "192.168.1.64": "Huuuha",
            "192.168.889.75": "TesT",
        }

    def addNewconnectedCar(self, clientIp):
        tmp = deepcopy(self.carDataSample)
        if clientIp in self.teams:
            index = self.teams[clientIp]
        else:
            index = clientIp
        self.connected.append(index)
        if not index in self.alldata:
            with self.lock:
                self.alldata[index] = tmp

    def removeCar(self, clientIp):
        if clientIp in self.connected:
            self.connected.remove(clientIp)
        else:
            self.connected.remove(self.teams[clientIp])

    def modifyData(self, client, toput):
        # Receives like: {"type": data/devicePos/deviceRot/deviceSpeed, "data":any}
        ip, port = client.split(":")
        if ip in self.teams:
            index = self.teams[ip]
        else:
            index = ip
        self.fileHandler.write(json.dumps(toput))
        with self.lock:
            if toput["type"] == "historyData":
                self.alldata[index]["historyData"].append(
                    [toput["value1"], toput["value2"], toput["value3"]]
                )
            elif toput["type"] == "devicePos":
                x_y = (toput["value1"], toput["value2"])
                self.alldata[index]["devicePos"] = x_y
            elif toput["type"] == "deviceRot" or toput["type"] == "deviceSpeed":
                self.alldata[index]["deviceRot"] = toput["value1"]

    def getDeviceIP(self, id):
        return self.devices[id]

    def getConnections(self):
        with self.lock:
            tmp = list(self.alldata.keys())
        return tmp

    def getConnectionData(self, client):
        with self.lock:
            tmp = deepcopy(self.alldata[client])
        return tmp

    def getConnectedNow(self):
        return self.connected

    def close(self):
        self.fileHandler.close()
