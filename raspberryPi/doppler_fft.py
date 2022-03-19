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
#   2. Sets configuration
#   3. Starts data acquisition
#   4. Fetches samples from BGT60LTR11
#   5. Stops data acquisition
#   6. Deinterleaves data
#   7. Performs mean removal
#   8. Applies window function
#   9. Computes Doppler spectrum
#   10. Plots Doppler spectrum
#
# Dependencies:
#   - matplotlib, scipy: For this script you need scipy and matplotlib installed. You can
#     install both either using pip:
#         $ pip install scipy matplotlib
#     or you use the Anaconda Python distribution which already includes
#     matplotlib: https://www.anaconda.com/products/individual

from ltr11 import *
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

if __name__ == "__main__":
    num_samples = 512                            # 512 samples
    window = signal.chebwin(num_samples, at=150) # Chebychev window
    sampling_frequency = 2000                    # sampling frequency of 2kHz

    device_config = {
        "mode": 0,           # continuous wave mode
        "tx_power_level": 7, # 4.5dBm
        "rx_if_gain": 8,     # 50dB
        "adc": 1,            # ADCs of RadarBaseboardMCU7
        "sampling_frequency": sampling_frequency
    }

    # 1. open the device
    with BGT60LTR11() as ltr11:
        # 2. set configuration
        ltr11.set_configuration(**device_config)

        # 3. start data acquisition
        ltr11.start_data_acquisition()

        # 4. fetch num_samples of samples (IFI and IFQ values)
        #    first fetch 1000 samples such that the BGT60LTR11 to avoid
        #    transient phenomena.
        ltr11.get_data(1000)
        ifi, ifq = ltr11.get_data(num_samples)

        # 5. stop data acquisition
        ltr11.stop_data_acquisition()

    # 6. deinterleave the data
    signal_complex = ifi + 1j*ifq

    # 7. perform mean removal
    signal_complex -= np.mean(signal_complex)

    # 8. apply window
    signal_complex *= window

    # 9. compute Doppler spectrum
    doppler = 10*np.log10(np.abs(np.fft.fft(signal_complex)))
    frequency = np.fft.fftfreq(num_samples, 1/sampling_frequency)

    # 10. plot Doppler spectrum
    # Note that the fftshift is just needed to avoid an extra line in the plot,
    # see
    # https://stackoverflow.com/questions/39837495/got-an-extra-line-on-python-plot/39839205
    # for an explanation.
    #
    # Approaching targets result in a peak at positive frequencies, departing
    # targets result in a peak at negative frequencies.
    plt.plot(np.fft.fftshift(frequency), np.fft.fftshift(doppler))
    plt.xlabel("frequency [Hz]")
    plt.ylabel("Doppler spectrum [dB]")
    plt.show()
