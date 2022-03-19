# ===========================================================================
# Copyright (C) 2021 Infineon Technologies AG
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===========================================================================

# This script does the following:
#   1. Opens BGT60LTR11 radar device
#   2. Reads current configuration from the device and prints it.
#   3. Reads the current detection status and prints it.
#   4. Starts the data acquisition.
#   5. Fetches IFI and IFQ data from the BGT60LTR11.
#   6. Stops data acquisition.
#   7. Plots the IFI and IFQ data.
#
# Dependencies:
#   - matplotlib: For this script you need matplotlib installed. You can
#     install matplotlib either using pip:
#         $ pip install matplotlib
#     or you use the Anaconda Python distribution which already includes
#     matplotlib: https://www.anaconda.com/products/individual

from ltr11 import *
import matplotlib.pyplot as plt
from print_config import config2string
import smbus
import time
rpi = smbus.SMBus(1)
time.sleep(1)
arduino = 0x8
def writeData(value):
    rpi.write_byte(arduino, ord(value))
    return -1

if __name__ == "__main__":
    # 1. open the device
    with BGT60LTR11() as ltr11:
        # 2. print the current configuration
        config = ltr11.get_configuration()
        print("Configuration:")
        print(config2string(ltr11, config))
        last_detection = ltr11.get_detection()
        writeData(last_detection.direction[0])
        # 3. print detection status
        while True:
            detection = ltr11.get_detection()
            print("Detection status: motion={}, direction={}".format(
                detection.motion, detection.direction))
            if(detection.direction!=last_detection.direction):
                writeData(detection.direction[0])
                last_detection=detection
        # 4. start data acquisition
        ltr11.start_data_acquisition()

        # 5. fetch 1024 samples (IFI and IFQ values) from device
        #    len(data) will be 2*1024=2048
        ifi, ifq = ltr11.get_data(num_samples=1024)

        # 6. stop data acquisition
        ltr11.stop_data_acquisition()

    # 7. plot IFI and IFQ signal
    plt.plot(ifi, label="I")
    plt.plot(ifq, label="Q")
    plt.legend()
    plt.xlabel("sample number")
    plt.ylabel("signal")

    plt.show()
