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

# The server itself. Creates a new Protocol for each new connection and has the info for all of them.
class tcpServer(protocol.Factory):
    def __init__(self, data_dealer, location_dealer):
        self.connections = {}  # dictionary to store the connections
        self.data_dealer = data_dealer  # instance of data dealer
        self.location_dealer = location_dealer  # instance of location dealer

    def send_data_to_client(self, client, message):
        try:
            self.connections[client].send_data(message)  # send data to a specific client
        except:
            print("Client not connected")

    def send_location(self, locID, client):
        msg = self.location_dealer.getLocation(locID)  # get location data from location dealer
        msg["type"] = "location"
        self.connections[client].send_data(msg)  # send location data to a specific client

    def receive_data_from_client(self, client, message):
        try:
            array_m = message.replace("}{", "}}{{").split("}{")  # split the message into individual JSON objects
            for mg in array_m:
                msg = json.loads(mg)  # parse each JSON object
                if msg["reqORinfo"] == "request":
                    msg["error"] = "request not recognised."
                    self.send_data_to_client(client, msg)  # send error message to client
                elif msg["reqORinfo"] == "info":
                    if msg["type"] == "devicePos":
                        if "value1" not in msg or "value2" not in msg:
                            msg["error"] = "Missing 'value1' or 'value2' in message."
                            self.send_data_to_client(client, msg)
                            return
                        self.data_dealer.modifyData_devicePos(client, msg)  # modify data based on message type
                    elif msg["type"] == "deviceRot":
                        if "value1" not in msg:
                            msg["error"] = "Missing 'value1' in message."
                            self.send_data_to_client(client, msg)
                            return
                        self.data_dealer.modifyData_deviceRot(client, msg)
                    elif msg["type"] == "deviceSpeed":
                        if "value1" not in msg:
                            msg["error"] = "Missing 'value1' in message."
                            self.send_data_to_client(client, msg)
                            return
                        self.data_dealer.modifyData_deviceSpeed(client, msg)
                    elif msg["type"] == "historyData":
                        if "value1" not in msg or "value2" not in msg or "value3" not in msg:
                            msg["error"] = "Missing 'value1' or 'value2' or 'value3' in message."
                            self.send_data_to_client(client, msg)
                            return
                        self.data_dealer.modifyData_historyData(client, msg)
                    elif msg["type"] == "locIDsub":
                        if "freq" not in msg or "locID" not in msg:
                            msg["error"] = "Missing 'freq' or 'locID' in message."
                            self.send_data_to_client(client, msg)  # send error message to client
                            return
                        freq = msg["freq"]
                        if 0.2 > freq or 5 < freq:
                            msg["error"] = "Frequency must be between 0.2 and 5."
                            self.send_data_to_client(client, msg)  # send error message to client
                            return
                        if not self.location_dealer.isConnecedDev(msg["locID"]):
                            msg["error"] = "Location ID not connected."
                            self.send_data_to_client(client, msg)
                            return
                        self.connections[client].loopingStream = task.LoopingCall(self.send_location, msg["locID"], client)  # start sending location data at specified frequency
                        self.connections[client].loopingStream.start(freq)                               
                    elif msg["type"] == "locIDubsub":
                        self.connections[client].loopingStream.stop()  # stop sending location data
                        del self.connections[client].loopingStream
                        return
                    else:
                        msg["error"] = "request not recognised."
                        self.send_data_to_client(client, msg)  # send error message to client
                else:
                    msg["error"] = "Message not recognized, 'reqORinfo' missing"
                    self.send_data_to_client(client, msg)  # send error message to client
        except Exception as e:
            print("error from ", client, " with ", e)

    def doStop(self):
        self.data_dealer.close()  # close the data dealer

    def buildProtocol(self, addr):
        self.data_dealer.addNewconnectedCar(addr.host)  # add new connected car to data dealer
        conn = SingleConnection()
        conn.factory = self
        return conn


# One class is generated for each new connection
class SingleConnection(protocol.Protocol):
    def connectionMade(self):
        peer = self.transport.getPeer()
        self.connectiondata = peer.host + ":" + str(peer.port)  # store connection data
        self.factory.connections[self.connectiondata] = self  # add connection to server's connections dictionary
        print("Connection with :", self.connectiondata, " established")

    def dataReceived(self, data):
        self.factory.receive_data_from_client(self.connectiondata, data.decode())  # process received data

    def connectionLost(self, reason):
        print("Connection lost with ", self.connectiondata, " due to: ", reason)
        try: 
            self.factory.connections[self.connectiondata].loopingStream.stop()  # stop sending location data
            self.factory.data_dealer.removeCar(self.connectiondata.split(":")[0])  # remove car from data dealer
        except: pass
        del self.factory.connections[self.connectiondata]  # remove connection from server's connections dictionary

    def send_data(self, message):
        msg = json.dumps(message)
        self.transport.write(msg.encode())  # send data to client