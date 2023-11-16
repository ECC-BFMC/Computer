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

from twisted.internet import reactor

from udpStream import udpStream
from tcpServer import tcpServer
from locsys_SIM import tcpServerLocsys
from Useful.dataDealer import dataDealer
from Useful.periodicTask_test import periodicTask

class TrafficCommunication():
    def __init__(self, encrypt_key, streamPort=9000, commPort=5000):

        self.data_dealer = dataDealer()

        self.tcp_factory_Locsys = tcpServerLocsys()
        self.tcp_factory = tcpServer(self.data_dealer)
        self.udp_factory = udpStream(streamPort, commPort, encrypt_key)
        self.period_task = periodicTask(0.1, self.data_dealer)

        self.reactor = reactor

        self.reactor.listenTCP(commPort, self.tcp_factory)
        self.reactor.listenTCP(4691, self.tcp_factory_Locsys)
        self.reactor.listenUDP(streamPort, self.udp_factory)

    def run(self):
        self.period_task.start()
        # self.reactor.run(installSignalHandlers=False)

    def stop(self):
        self.period_task.stop()
        self.reactor.stop()


if __name__ == "__main__":
    filename = "src/servers/trafficCommunicationServer/Useful/privatekey_server_test.pem"
    traffic_communication = TrafficCommunication(filename)
    traffic_communication.run()
    from multiprocessing import Event

    blocker = Event()

    try:
        blocker.wait()
    except KeyboardInterrupt:
        print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
        traffic_communication.stop()

