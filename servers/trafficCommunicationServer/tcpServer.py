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

from twisted.internet import protocol
import json


# The server itself. Creates a new Protocol for each new connection and has the info for all of them.
class tcpServer(protocol.Factory):
    def __init__(self, data_dealer):
        self.connections = {}
        self.data_dealer = data_dealer

    def send_data_to_client(self, client, message):
        try:
            self.connections[client].send_data(message)
        except:
            print("Client not connected")

    def receive_data_from_client(self, client, message):
        try:
            array_m = message.replace("}{", "}}{{").split("}{")
            for mg in array_m:
                msg = json.loads(mg)
                if msg["reqORinfo"] == "request":
                    if msg["type"] == "locsysDevice":
                        try:
                            msg["response"] = self.data_dealer.getDeviceIP(
                                msg["DeviceID"]
                            )
                        except:
                            msg["error"] = "DeviceID not found in list."
                    else:
                        msg["error"] = "request not recognised."
                    self.send_data_to_client(client, msg)
                elif msg["reqORinfo"] == "info":
                    if (
                        msg["type"] == "devicePos"
                        or msg["type"] == "deviceRot"
                        or msg["type"] == "deviceSpeed"
                        or msg["type"] == "historyData"
                    ):
                        self.data_dealer.modifyData(client, msg)
                    else:
                        msg["error"] = "request not recognised."
                        self.send_data_to_client(client, msg)
                else:
                    msg["error"] = "Message not recognized, 'reqORinfo' missing"
                    self.send_data_to_client(client, msg)
        except Exception as e:
            print("error from ", client, " with ", e)

    def doStop(self):
        self.data_dealer.close()

    def buildProtocol(self, addr):
        self.data_dealer.addNewconnectedCar(addr.host)
        conn = SingleConnection()
        conn.factory = self
        return conn


# One class is generated for each new connection
class SingleConnection(protocol.Protocol):
    def connectionMade(self):
        peer = self.transport.getPeer()
        self.connectiondata = peer.host + ":" + str(peer.port)
        self.factory.connections[self.connectiondata] = self
        print("Connection with :", self.connectiondata, " established")

    def dataReceived(self, data):
        print(data.decode())
        self.factory.receive_data_from_client(self.connectiondata, data.decode())

    def connectionLost(self, reason):
        print("Connection lost with ", self.connectiondata, " due to: ", reason)
        del self.factory.connections[self.connectiondata]

    def send_data(self, message):
        print(message)
        msg = json.dumps(message)
        self.transport.write(msg.encode())
