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
from twisted.internet import reactor
from udpStream import udpStream
from tcpServer import tcpServer
from locsys_SIM import LocsysGather
from Useful.dataDealer import dataDealer
from Useful.periodicTask_test import periodicTask
from Useful.locationDealer import locationDealer

class TrafficCommunication():
    def __init__(self, encrypt_key, streamPort=9000, commPort=5000):
        # Initialize data dealer and location dealer
        self.data_dealer = dataDealer()
        self.location_dealer = locationDealer()

        # Initialize LocsysGather with location dealer
        self.Locsys = LocsysGather(self.location_dealer)

        # Initialize tcpServer with data dealer and location dealer
        self.tcp_factory = tcpServer(self.data_dealer, self.location_dealer)

        # Initialize udpStream with streamPort, commPort, and encrypt_key
        self.udp_factory = udpStream(streamPort, commPort, encrypt_key)

        # Initialize periodicTask with data dealer
        self.period_task = periodicTask(0.1, self.data_dealer, self.location_dealer)

        # Initialize reactor
        self.reactor = reactor

        # Listen for TCP connections on commPort
        self.reactor.listenTCP(commPort, self.tcp_factory)

        # Listen for UDP connections on streamPort
        self.reactor.listenUDP(streamPort, self.udp_factory)

    def run(self):
        # Start periodic task
        self.period_task.start()

        # Run the reactor
        self.reactor.run()

    def stop(self):
        # Stop LocsysGather
        self.Locsys.stop()

        # Stop periodic task
        self.period_task.stop()


if __name__ == "__main__":
    # Specify the filename for the private key
    filename = "Useful/privatekey_server_test.pem"

    # Create an instance of TrafficCommunication
    traffic_communication = TrafficCommunication(filename)

    # Run the traffic communication
    traffic_communication.run()

    traffic_communication.stop()
