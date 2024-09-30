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
import threading
import copy

class locationDealer:
    def __init__(self):
        # Initialize the devices dictionary
        self.devices = {}

    def connectDev(self, IDloc):
        # Add a new device to the devices dictionary
        self.devices[IDloc] = {}
        self.devices[IDloc]["lock"] = threading.Lock()
        self.devices[IDloc]["pos"] = {"x":0.0, "y":0.0, "z":0.0, "quality":0}
    
    def disconnectDev(self, IDloc):
        # Remove a device from the devices dictionary
        del self.devices[IDloc]

    def getLocation(self, IDloc):
        # Get the location of a device
        with self.devices[IDloc]["lock"]:
            tmp = copy.deepcopy(self.devices[IDloc]["pos"])
        return tmp
    
    def getLocations(self):
        a = {}
        for device in self.devices:
            a[device] = {}
            with self.devices[device]["lock"]:
                a[device]["pos"] =  tmp = copy.deepcopy((self.devices[device]["pos"]))
        return a
    

    def isConnecedDev(self, IDloc):
        # Check if a device is connected
        return IDloc in self.devices
    
    def updateLocation(self, IDloc, x, y, quality, z = 2.3):
        # Update the location of a device
        with self.devices[IDloc]["lock"]:
            self.devices[IDloc]["pos"] = {"x":x, "y":y, "z":z, "quality":quality}
