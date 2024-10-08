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
from twisted.internet import task


class periodicTask(task.LoopingCall):
    def __init__(self, interval, data_dealer, location_dealer):
        super().__init__(self.periodicCheck)
        self.interval = interval
        self.data_dealer = data_dealer
        self.location_dealer = location_dealer

    def start(self):
        super().start(self.interval)

    def periodicCheck(self):
        # Get all clients connected to the server
        allClients = self.data_dealer.getConnections()
        
        # Get currently connected clients
        connectedClients = self.data_dealer.getConnectedNow()

        positions = self.location_dealer.getLocations()
        
        # Clear the console
        print ("\033c")
        
        # Print server status
        print("Server: ON")
        
        # Print the connected clients
        print("The connected clients are:", connectedClients)
        
        # Print all-time data since startup
        print("THE ALLTIMEDATA (since startup) IS: ")
        print("-------------------------------------------")
        
        # Print data for each client
        for client in allClients:
            data = self.data_dealer.getConnectionData(client)
            print("+ + + ", client, " data is: ", data)
        
        print("-------------------------------------------")

        print("THE device/s location is:  \n")
         # Print data for each device
        for position in positions:
            print(position, "+ + + ", positions[position], " + + +\n")

        print("To quit, press Ctrl+C")
