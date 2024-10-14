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
# Import necessary modules
from .fileHandler import FileHandler
import threading
from collections import deque
from copy import deepcopy
import json

class dataDealer:
    def __init__(self):
        # Initialize instance variables
        self.lock = threading.Lock()  # Lock for thread safety
        self.alldata = {}  # Dictionary to store all data
        self.connected = []  # List to store connected devices
        self.fileHandler = FileHandler("historyFile.txt")  # File handler for history file
        data_points = deque(maxlen=30)  # Creates and handles a list of maximum 30 points, discarding old ones when appending new data.
        self.carDataSample = {
            "devicePos": (0.0, 0.0),
            "deviceRot": 0.0,
            "deviceSpeed": 0.0,
            "historyData": data_points,
        }  # Sample data structure for a connected car

        self.teams = {
            "192.168.1.61": "Popa",
            "192.168.1.62": "Lopa",
            "192.168.1.63": "Mopa",
            "192.168.1.64": "Huuuha",
            "192.168.889.75": "TesT"
        }  # Dictionary to store team names based on IP addresses

    def addNewconnectedCar(self, clientIp):
        # Add a new connected car to the data dealer
        tmp = deepcopy(self.carDataSample)  # Create a deep copy of the carDataSample
        if clientIp in self.teams:
            index = self.teams[clientIp]  # Get the team name based on the client IP
        else:
            index = clientIp  # Use the client IP as the index
        self.connected.append(index)  # Add the index to the connected list
        if not index in self.alldata:
            with self.lock:
                self.alldata[index] = tmp  # Add the new car data to the alldata dictionary

    def removeCar(self, clientIp):
        # Remove a car from the connected list
        if clientIp in self.connected:
            self.connected.remove(clientIp)  # Remove the client IP from the connected list
        else:
            self.connected.remove(self.teams[clientIp])  # Remove the team name based on the client IP

    def modifyData_devicePos(self, client, toput):
        # Modify the device position data based on the received input
        ip, port = client.split(":")  # Split the client IP and port
        if ip in self.teams:
            index = self.teams[ip]  # Get the team name based on the IP
        else:
            index = ip  # Use the IP as the index
        self.fileHandler.write(json.dumps(toput))  # Write the data to the history file
        with self.lock:
            x_y = (toput["value1"], toput["value2"])
            self.alldata[index]["devicePos"] = x_y  # Update the car's devicePos

    def modifyData_deviceRot(self, client, toput):
        # Modify the device rotation data based on the received input
        ip, port = client.split(":")  # Split the client IP and port
        if ip in self.teams:
            index = self.teams[ip]  # Get the team name based on the IP
        else:
            index = ip  # Use the IP as the index
        self.fileHandler.write(json.dumps(toput))  # Write the data to the history file
        with self.lock:
            self.alldata[index]["deviceRot"] = toput["value1"]  # Update the car's deviceRot

    def modifyData_deviceSpeed(self, client, toput):
        # Modify the device speed data based on the received input
        ip, port = client.split(":")  # Split the client IP and port
        if ip in self.teams:
            index = self.teams[ip]  # Get the team name based on the IP
        else:
            index = ip  # Use the IP as the index
        self.fileHandler.write(json.dumps(toput))  # Write the data to the history file
        with self.lock:
            self.alldata[index]["deviceSpeed"] = toput["value1"]  # Update the car's deviceSpeed

    def modifyData_historyData(self, client, toput):
        # Modify the history data based on the received input
        ip, port = client.split(":")  # Split the client IP and port
        if ip in self.teams:
            index = self.teams[ip]  # Get the team name based on the IP
        else:
            index = ip  # Use the IP as the index
        self.fileHandler.write(json.dumps(toput))  # Write the data to the history file
        with self.lock:
            self.alldata[index]["historyData"].append(
                [toput["value1"], toput["value2"], toput["value3"]]
            )  # Append the history data to the car's historyData list

    def getConnections(self):
        # Get the list of connected devices
        with self.lock:
            tmp = list(self.alldata.keys())
        return tmp

    def getConnectionData(self, client):
        # Get the data for a specific connected device
        with self.lock:
            tmp = deepcopy(self.alldata[client])
        return tmp

    def getConnectedNow(self):
        # Get the list of currently connected devices
        return self.connected

    def close(self):
        # Close the file handler
        self.fileHandler.close()
