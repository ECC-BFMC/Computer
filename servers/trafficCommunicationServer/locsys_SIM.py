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
from twisted.internet import task
import itertools
import re

# Function to extract positions from log file
def extract_positions_from_log(log_file_path):
    positions = []
    pattern = re.compile(r"'x': '([-+]?\d*\.\d+|\d+)', 'y': '([-+]?\d*\.\d+|\d+)', 'quality': (\d+)")
    
    with open(log_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                quality = int(match.group(3))
                positions.append((x, y, quality))
    return positions

class LocsysGather():
    def __init__(self, location_dealer):
        # Set the path to the log file
        self.path = extract_positions_from_log("Useful/sample_data.txt")
        # Set the frequency of data update
        self.frequency = 0.2
        # Initialize connections dictionary
        self.connections = {}
        # Set the location dealer
        self.location_dealer = location_dealer
        # set the simulated device
        self.device = 3
        # Connect to the device
        self.location_dealer.connectDev(self.device)
        # Create an iterator to cycle through the positions array
        self.array_iterator = itertools.cycle(self.path)

        # Start a looping call to update data at the specified frequency
        self.streaming_task = task.LoopingCall(self.update_data)
        self.streaming_task.start(self.frequency)

    def update_data(self):
        # Get the next position from the iterator
        pos = next(self.array_iterator)
        # Update the location dealer with the new position
        self.location_dealer.updateLocation(self.device, pos[0], pos[1], pos[2])

    def stop(self):
        # Disconnect from the device with ID 3
        self.location_dealer.disconnectDev(self.device)
        # Stop the streaming task
        self.streaming_task.stop()
