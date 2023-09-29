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

from .threadwithstop import ThreadWithStop
from twisted.internet import reactor, protocol, task
import time
import json
import numpy as np


class threadRemoteHandlerPC(ThreadWithStop):
    """This thread will handle the connection between Demo and raspberry PI

    Args:
        pipeRecv (multiprocessing.pipe.Pipe): Receving pipe
        pipeSend (multiprocessing.pipe.Pipe): Sending pipe
        Ip(String): Ip to connect
        Port(String) : port to connect
        Passw(String) : Passw to conect
    """

    def __init__(self, pipeRecv, pipeSend, Ip, Port, Passw):
        super(threadRemoteHandlerPC, self).__init__()
        self.pipeSend = pipeSend
        self.factory = FactoryDealer(self.pipeSend, Passw)
        self.reactor = reactor
        self.reactor.connectTCP(Ip, Port, self.factory)
        self.task = PeriodicTask(
            self.factory, 0.1, pipeRecv
        )  # Replace X with the desired number of seconds

    def run(self):
        self.task.start()
        self.reactor.run(installSignalHandlers=False)

    def stop(self):
        super(threadRemoteHandlerPC, self).stop()
        self.reactor.stop()


import base64


# One class is generated for each new connection
class SingleConnection(protocol.Protocol):
    def connectionMade(self):
        """This function will be called only if the connection was made."""
        peer = self.transport.getPeer()
        self.factory.connectiondata = peer.host + ":" + str(peer.port)
        print("Trying connection with server :", self.factory.connectiondata)
        self.factory.isConnected = True
        self.factory.connection = self
        self.send_data(self.factory.passw)
        self.buffer = b""
        self.state = "SIZE&TYPE"
        self.size = 0

    def dataReceived(self, data):
        """This function will be called only when we receive a pack of data.

        Args:
            data (string): this will be the pack of data received.
        """
        self.buffer += data
        if self.state == "SIZE&TYPE":
            if len(self.buffer) >= 5:  # is_json 5
                self.type = int.from_bytes(self.buffer[:1], byteorder="big")
                self.size = int.from_bytes(self.buffer[2:5], byteorder="big")
                self.buffer = self.buffer[5:]
                if self.type == 1:
                    self.state = "ENABLEBUTTON"
                elif self.type == 2:
                    self.state = "ENGINERUNNING"
                elif self.type == 3:
                    self.state = "LOCATION"
                elif self.type == 4:
                    self.state = "SIGNAL"
                elif self.type == 5:
                    self.state = "IMAGE"
        elif self.state == "IMAGE":
            if len(self.buffer) >= self.size:
                img_data = self.buffer[: self.size]
                self.buffer = self.buffer[self.size :]
                decoded_bytes = base64.b64decode(img_data)
                nparr = np.fromstring(
                    decoded_bytes, np.uint8
                )  # Convert bytes to numpy array
                self.factory.pipeSend.send({"action": "modImg", "value": nparr})
                self.state = "SIZE&TYPE"
        elif self.state == "ENABLEBUTTON":
            if len(self.buffer) >= self.size:
                data = self.buffer[: self.size]
                dat = data.decode("utf-8")
                self.buffer = self.buffer[self.size :]
                self.factory.pipeSend.send({"action": "engStart", "value": dat})
                self.state = "SIZE&TYPE"
        elif self.state == "ENGINERUNNING":
            if len(self.buffer) >= self.size:
                data = self.buffer[: self.size]
                dat = data.decode("utf-8")
                self.buffer = self.buffer[self.size :]
                self.factory.pipeSend.send({"action": "engRunning", "value": dat})
                self.state = "SIZE&TYPE"
        elif self.state == "LOCATION":
            if len(self.buffer) >= self.size:
                data = self.buffer[: self.size]
                dat = data.decode("utf-8")
                self.buffer = self.buffer[self.size :]
                datajson = json.loads(dat)
                self.factory.pipeSend.send({"action": "map", "value": datajson})
                self.state = "SIZE&TYPE"
        elif self.state == "SIGNAL":
            if len(self.buffer) >= self.size:
                data = self.buffer[: self.size]
                dat = data.decode("utf-8")
                self.buffer = self.buffer[self.size :]
                self.state = "SIZE&TYPE"

    def connectionLost(self, reason):
        """This function will be called when we lost connection.

        Args:
            reason (String): Reason of losing connection.
        """
        self.factory.isConnected = False
        self.factory.connection = None
        self.factory.pipeSend.send({"action": "enableStartEngine", "value": False})
        self.factory.pipeSend.send({"action": "emptyAll", "value": False})
        print(
            "Connection lost with server ",
            self.factory.connectiondata,
            " due to: ",
            reason,
        )

    def send_data(self, message):
        """We use this function to send messages.

        Args:
            message (String): message to be send
        """
        if isinstance(message, dict):
            msg = json.dumps(message)
        else:
            msg = message

        self.transport.write(msg.encode())


# The server itself. Creates a new Protocol for each new connection and has the info for all of them.
class FactoryDealer(protocol.ClientFactory):
    """This class handle sending informations.
    Args:
        pipeSend (multiprocessing.pipe.Pipe): Pipe for sending data.
        passw (String): Password t oconnect.
    """

    def __init__(self, pipeSend, passw):
        self.connection = None
        self.isConnected = False
        self.retry_delay = 1
        self.pipeSend = pipeSend
        self.passw = passw

    def send_data_to_client(self, message):
        """If client is connected this function will send the message to the connected device.

        Args:
            message (String): Message to be send.
        """
        if self.isConnected == True:
            self.connection.send_data(message)
        else:
            print("Not connected to server")

    def clientConnectionLost(self, connector, reason):
        print(
            "Connection lost with server ",
            self.connectiondata,
            " Retrying in ",
            self.retry_delay,
            " seconds... (Check password match, IP or server availability)",
        )
        self.connectiondata = None
        time.sleep(self.retry_delay)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed. Retrying in", self.retry_delay, "seconds...")
        time.sleep(self.retry_delay)
        connector.connect()

    def buildProtocol(self, addr):
        conn = SingleConnection()
        conn.factory = self
        return conn


# The interface between the server and the gateway
class PeriodicTask(task.LoopingCall):
    def __init__(self, factory, interval, pipeRecv):
        super().__init__(self.periodicCheck)
        self.factory = factory
        self.interval = interval
        self.pipeRecv = pipeRecv

    def start(self):
        # Subscribing to the desired messages and adding all the pipes to a list
        super().start(self.interval)

    def stop(self):
        if self.running:
            super().stop()

    def periodicCheck(self):
        if self.pipeRecv.poll():
            msg = self.pipeRecv.recv()
            self.factory.send_data_to_client(msg)


if __name__ == "__main__":
    allProcesses = list()

    server_thread = threadRemoteHandlerPC("outps", "ints")
    allProcesses.append(server_thread)

    print("Starting the processes!", allProcesses)
    for proc in allProcesses:
        proc.start()

    from multiprocessing import Event

    blocker = Event()

    try:
        blocker.wait()
    except KeyboardInterrupt:
        print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
        for proc in allProcesses:
            if hasattr(proc, "stop") and callable(getattr(proc, "stop")):
                print("Process with stop", proc)
                proc.stop()
                proc.join()
            else:
                print("Process witouth stop", proc)
                proc.terminate()
                proc.join()
