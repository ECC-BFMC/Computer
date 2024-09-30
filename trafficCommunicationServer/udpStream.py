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
from twisted.internet import task, protocol
from Useful import keyDealer as keyDealer

# Define the udpStream class
class udpStream(protocol.DatagramProtocol):
    def __init__(self, streamPort, commPort, encrypt_key, frequency=1):
        # Set the broadcast address and stream frequency
        self.address = ("<broadcast>", streamPort)
        self.frequency = frequency

        # Load the private key and prepare the message to send
        key = keyDealer.load_private_key(encrypt_key)
        msg = "listening on:" + str(commPort)
        msg_t = msg.encode()
        signature = keyDealer.sign_data(key, msg_t)
        tmpMsgToSend = signature + "(-.-)".encode() + msg_t
        self.MsgToSend = tmpMsgToSend

    def startProtocol(self):
        # Allow broadcasting and start the streaming task
        self.transport.setBroadcastAllowed(True)
        self.streaming_task = task.LoopingCall(self.send_message)
        self.streaming_task.start(self.frequency)  # Send data every 1 second

    def send_message(self):
        # Send the message to the broadcast address
        self.transport.write(self.MsgToSend, self.address)

    def connectionLost(self, reason):
        # Stop the streaming task when the server is stopped
        self.streaming_task.stop()
