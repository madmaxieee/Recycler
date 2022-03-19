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

"""
Python wrapper for BGT60LTR11AIP

Overview
--------

This Python module allows you to easily access the Infineon BGT60LTR11AIP radar
sensor. The main functionality includes:
  - Configuring the BGT60LTR11AIP and reading back the configuration.
  - Fetching the IFI and IFQ signal.
  - Reading the status of the internal motion detector.
  - Reading and writing arbitrary registers of the BGT60LTR11AIP.
  - Performing a soft-reset.

Hardware setup
--------------

Please make sure that the BGT60LTR11AIP is plugged into the socket of the
RadarBaseboardMCU7 board on the upper side (side 1; the side with the black
Atmel microcontroller). For RF Shield V2.0, it's also possible to connect it 
to the backside (side2). A white filled circle is drawn as a marker for both 
BGT60LTR11AIP shield, and Radar Baseboard MCU7 board. These markers must be aligned
to plug in the sensor board correctly, for more details please refer to the AN599.

Connect the RadarBaseboardMCU7 using a USB cable to your computer. 
On success, when motion is detected, both BGT60LTR11AIP shield, and RadarBaseboardMCU7 board can indicate detection status via LEDs: 
    - RadarBaseboardMCU7: LED is OFF when no target, and is red/green if a departing/approaching target is detected.
    - BGT60LTR11AIP shield: green LED is ON when a target is detected, and red LED is ON/OFF when a target is departing/approaching from the sensor.

Dependencies
------------

This wrapper requires Python 3 and numpy. The wrapper works on following
platforms:
  * Windows 10 with 64bit Python
  * Raspberry Pi, Raspbian GNU/Linux 10
  * Ubuntu 20.04, x86-64

You can install numpy either using pip

    $ pip install numpy

or you can install the Anaconda Python distribution which includes among others
the NumPy module: https://www.anaconda.com/products/individual

Documentation
-------------
You can view this documentation using pdoc:

    $ pdoc -d numpy ./ltr11.py
"""


from ctypes import *
import numpy as np
from collections import namedtuple
import os
import sys
import time
import platform

# by default,
#   from BGT60LTR11 import *
# would import all objects, including the ones from ctypes. To avoid name space
# pollution, we list what symbols should be exported.
__all__ = ["BGT60LTR11Error", "BGT60LTR11FIFOError",
           "BGT60LTR11Detection", "BGT60LTR11"]


class BGT60LTR11Error(Exception):
    """BGT60LTR11 exception class"""
    pass


class BGT60LTR11FIFOError(BGT60LTR11Error):
    """BGT60LTR11FIFO exception class"""
    pass


BGT60LTR11Detection = namedtuple(
    "BGT60LTR11Detection", ["motion", "direction"])
BGT60LTR11Detection.__doc__ = '''\
Detection state of BGT60LTR11AIP

Members:
- ``motion``: bool describing if motion was detected
- ``direction``: direction of the motion (either "approach" or "depart")

If ``motion`` is False the value of direction might be either "approach" or
"depart".

``motion`` is True if the green LED on the BGT60LTR11AIP shield is on, otherwise
False.

``direction`` is "depart" if the red LED on the BGT60LTR11AIP shield is on,
otherwise "approach".'''


class Bgt60ltr11Config(Structure):
    _fields_ = (('mode', c_int),
                ('pulse_width', c_int),
                ('pulse_repetition', c_int),
                ('hold_time', c_int),
                ('detection_threshold', c_uint8),
                ('tx_power_level', c_uint8),
                ('rx_if_gain', c_uint8),
                ('adc', c_int),
                ('sampling_frequency', c_uint32),
                ('rf_center_freq', c_uint8))


class BGT60ltr11DeviceInfo(Structure):
    _fields_ = [('description', POINTER(c_char_p)),
                ('min_rf_frequency_kHz', c_uint32),
                ('max_rf_frequency_kHz', c_uint32),
                ('num_tx_antennas', c_uint8),
                ('num_rx_antennas', c_uint8),
                ('max_tx_power', c_uint8),
                ('num_temp_sensors', c_uint8),
                ('major_version_hw', c_uint8),
                ('minor_version_hw', c_uint8),
                ('interleaved_rx', c_uint8),
                ('data_format', POINTER(c_uint8))

                ]


# absolute path to library (*.dll or *.so depending on the platform)
# we expect that the library is in the same directory as this file
if os.name == "nt":
    # If on Windows we require a 64bit system
    if sys.maxsize < 2**32:
        raise RuntimeError("This module requires a 64bit version of Python")
    libname = "ltr11.dll"
elif platform.system() == "Linux":
    machine = platform.machine()
    if machine == "armv7l":
        libname = "libltr11_raspi.so"
    elif machine == "x86_64":
        libname = "libltr11_amd64.so"
    else:
        raise RuntimeError(f"Not supported platform: {machine}")
else:
    raise RuntimeError("Unsupported operating system: {}".format(platform.system()))

dllabspath = os.path.dirname(os.path.abspath(
    __file__)) + os.path.sep + libname
libltr = CDLL(dllabspath)

c_ltr11_open = libltr.ltr11_open
c_ltr11_open.restype = c_void_p
c_ltr11_open.argtypes = [c_char_p]

c_ltr11_close = libltr.ltr11_close
c_ltr11_close.restype = None
c_ltr11_close.argtypes = [c_void_p]

c_ltr11_get_list = libltr.ltr11_get_list
c_ltr11_get_list.restype = c_int32
c_ltr11_get_list.argtypes = [c_char_p, c_size_t]

c_ltr11_read_register = libltr.ltr11_read_register
c_ltr11_read_register.restype = c_bool
c_ltr11_read_register.argtypes = [c_void_p, c_uint8, POINTER(c_uint16)]

c_ltr11_write_register = libltr.ltr11_write_register
c_ltr11_write_register.restype = c_bool
c_ltr11_write_register.argtypes = [c_void_p, c_uint8, c_uint16]

c_ltr11_get_detection = libltr.ltr11_get_detection
c_ltr11_get_detection.restype = c_bool
c_ltr11_get_detection.argtypes = [c_void_p, POINTER(c_bool), POINTER(c_bool)]

c_ltr11_start_data_acquisition = libltr.ltr11_start_data_acquisition
c_ltr11_start_data_acquisition.restype = c_bool
c_ltr11_start_data_acquisition.argtypes = [c_void_p]

c_ltr11_stop_data_acquisition = libltr.ltr11_stop_data_acquisition
c_ltr11_stop_data_acquisition.restype = c_bool
c_ltr11_stop_data_acquisition.argtypes = [c_void_p]

c_ltr11_get_raw_data = libltr.ltr11_get_raw_data
c_ltr11_get_raw_data.restype = c_bool
c_ltr11_get_raw_data.argtypes = [c_void_p, POINTER(
    POINTER(c_double)), POINTER(c_size_t), POINTER(c_bool), c_uint16, c_uint16]

c_ltr11_soft_reset = libltr.ltr11_soft_reset
c_ltr11_soft_reset.restype = c_bool
c_ltr11_soft_reset.argtypes = [c_void_p]

c_ltr11_get_configuration = libltr.ltr11_get_configuration
c_ltr11_get_configuration.restype = c_bool
c_ltr11_get_configuration.argtypes = [c_void_p, POINTER(Bgt60ltr11Config)]

c_ltr11_set_configuration = libltr.ltr11_set_configuration
c_ltr11_set_configuration.restype = c_bool
c_ltr11_set_configuration.argtypes = [c_void_p, POINTER(Bgt60ltr11Config)]

c_ltr11_get_firmware_version = libltr.ltr11_get_firmware_version
c_ltr11_get_firmware_version.restype = c_bool
c_ltr11_get_firmware_version.argtypes = [c_void_p, POINTER(
    c_uint16), POINTER(c_uint16), POINTER(c_uint16)]

c_ltr11_get_device_info = libltr.ltr11_get_device_info
c_ltr11_get_device_info.restype = c_bool
c_ltr11_get_device_info.argtypes = [c_void_p, POINTER(BGT60ltr11DeviceInfo)]


class BGT60LTR11:
    """Python wrapper for BGT60LTR11AIP"""

    @staticmethod
    def get_list():
        """Get a list of available devices.

        Each element of the list can be given as argument port in the
        constructor to open a specific device.

        Note that only devices are found which are not yet opened. A device
        which is currently opened will not be found by this method.

        Returns
        -------
        port_list: list
            A list of ports that can be given to ``BGT60LTR11``.

        Example
        -------
        Opening the second device found:

            device_list = BGT60LTR11.get_list()
            assert len(device_list) >= 2
            with BGT60LTR11(port=device_list[1]) as ltr11:
                # ...
        """
        size = 2048
        buf = create_string_buffer(size)
        c_ltr11_get_list(buf, size)
        return buf.value.decode("ascii").split(";")

    def __init__(self, port=None):
        """Open connection to a BGT60LTR11AIP device.

        The constructor opens the specific port. If port is not given (or
        None), the first device found will be opened. If no device is found an
        ``BGT60LTR11Error`` is raised.

        The device is automatically closed when the object goes out of scope.
        The recommended way of opening and closing devices is using a context
        manager:

            with BGT60LTR11() as ltr11:
                # use ltr11 device

        If you want to close the device manually, you can do so using the del
        statement:

            ltr11 = BGT60LTR11()
            # use ltr11 object
            del ltr11 # close

        Note that the library is not thread-safe. Do not use this library from
        different threads.
        """
        if port:
            port_bytes = port.encode("ascii")
            self.handle = c_ltr11_open(c_char_p(port_bytes))
        else:
            self.handle = c_ltr11_open(None)
        if not self.handle:
            raise BGT60LTR11Error("Cannot open device")

        if not self.check_minimum_firmware_version(1, 1, 5):
            major, minor, build = self.get_firmware_version()
            version = f"{major}.{minor}.{build}"
            raise BGT60LTR11Error(
                f"Need at least firmware version 1.1.5; actual version is {version}")

    def get_firmware_version(self):
        """Get firmware version.

        Returns
        -------
        version: tuple
            tuple consisting of the major, minor, and build version.
        """
        major, minor, build = c_uint16(0), c_uint16(0), c_uint16(0)
        if not c_ltr11_get_firmware_version(self.handle, byref(major), byref(minor), byref(build)):
            raise BGT60LTR11Error("Could not get firmware version")

        return major.value, minor.value, build.value

    def get_device_info(self):
        """ 
        Get device info 
        Returns
        -------
        device_info: dict
            Device Information.
        """
        device_info = BGT60ltr11DeviceInfo()
        if not c_ltr11_get_device_info(self.handle, byref(device_info)):
            raise BGT60LTR11Error("Could not get device information")

        d = {}
        for field in device_info._fields_:
            d[field[0]] = getattr(device_info, field[0])

        return d

    def check_minimum_firmware_version(self, major, minor, build):
        """Check if firmware is at least major.minor.build.

        Returns
        -------
        flag: bool
            True if firmware version is at least major.minor.build, otherwise
            False.
        """
        x, y, z = self.get_firmware_version()
        if x > major:
            return True
        elif x < major:
            return False

        if y > minor:
            return True
        elif y < minor:
            return False

        if z >= build:
            return True
        else:
            return False

    def read_register(self, addr):
        """Read register of BGT60LTR11AIP.

        Read the content of the register with address given by addr.

        Parameters
        ----------
        addr : int
            BGT60LTR11AIP address

        Returns
        -------
        value: int
            Value of the register read.
        """
        v = c_uint16(0)
        if not c_ltr11_read_register(self.handle, c_uint8(addr), pointer(v)):
            raise BGT60LTR11Error("Could not read register")
        return v.value

    def write_register(self, addr, value):
        """Write to register of BGT60LTR11AIP.

        Write value to the register with address given by addr.

        Parameters
        ----------
        addr: int
            BGT60LTR11AIP address  
        value: int
            value to be written to this register
        """
        if not c_ltr11_write_register(self.handle, c_uint8(addr), c_uint16(value)):
            raise BGT60LTR11Error("Could not write register")

    def get_detection(self):
        """Read the detection state of the BGT60LTR11AIP.

        The method returns the namedtuple ``BGT60LTR11Detection`` with elements
        (motion, direction). motion is a boolean indicating if motion was
        detected. direction is either "approach" or "depart".

        Returns
        -------
        detection: ``BGT60LTR11Detection``
            Detection state.
        """
        gpio1 = c_bool(False)
        gpio2 = c_bool(False)
        if not c_ltr11_get_detection(self.handle, pointer(gpio1), pointer(gpio2)):
            raise BGT60LTR11Error("Could not read detection state")

        detection = gpio1.value
        if gpio2.value:
            direction = "depart"
        else:
            direction = "approach"

        return BGT60LTR11Detection(detection, direction)

    def start_data_acquisition(self):
        """Start data acquisition."""
        if not c_ltr11_start_data_acquisition(self.handle):
            raise BGT60LTR11Error("Could not start data acquisition")

    def stop_data_acquisition(self):
        """Stop data acquisition."""
        if not c_ltr11_stop_data_acquisition(self.handle):
            raise BGT60LTR11Error("Could not stop data acquisition")

    def soft_reset(self):
        """Perform a soft-reset."""
        if not c_ltr11_soft_reset(self.handle):
            raise BGT60LTR11Error("Could not perform soft-reset")

    def get_raw_data(self, num_samples=None):
        """Fetch raw data from BGT60LTR11AIP.

        This is a more low-level version of ``get_data``. If you are only
        interested in fetching IFI and IFQ data, use ``get_data`` instead.

        Make sure to call ``start_data_acquisition`` first.

        The method returns the tuple (overflow, data).

        The flag overflow is true if the internal buffer on the
        RadarBaseboardMCU7 overflowed. In this case the most recent samples are
        returned, but older samples are lost.

        data contains the interleaved I/Q signal, starting with the Q signal.
        To deinterleave the data, one can use following numpy code:

            overflow, raw_data = device.get_raw_data()
            ifq = raw_data[::2]  # Q signal
            ifi = raw_data[1::2] # I signal

        The signal is between 0 and 1, the average of the signal is
        approximately at 0.5.

        Parameters
        ----------
        num_samples: int
            If `num_samples` is given data contains `num_samples` of samples
            (num_samples of IFI and num_samples of IFQ values). If `num_samples`
            is `None` all samples currently available are returned.

            Setting `num_samples` to values larger than 2048 might result in
            FIFO overflows. If you need more than 2048 samples it is
            recommended to call this method multiple times.

        Returns
        -------
        overflow: bool
            Flag indicating if a FIFO overflow occured

        data: np.ndarray:
            Interleaved I/Q data
        """
        if num_samples:
            min_samples = max_samples = num_samples
        else:
            min_samples = 0
            max_samples = 4096

        while True:
            data = POINTER(c_double)()
            overflow = c_bool(False)
            nsamples = c_size_t(0)
            if not c_ltr11_get_raw_data(self.handle, byref(data), byref(nsamples), byref(overflow), min_samples, max_samples):
                raise BGT60LTR11Error("Could not get raw data")

            if nsamples.value > 0:
                return overflow.value, np.array([data[i] for i in range(2*nsamples.value)])

            # sleep 20ms and then check again for new data
            time.sleep(0.02)

    def get_data(self, num_samples):
        """Fetch IFI and IFQ data from BGT60LTR11AIP.

        Make sure to call ``start_data_acquisition`` first.

        The method returns the IFI and IFQ data from the BGT60LTR11 as a
        tuple (ifi, ifq).

        In case of a FIFO overflow a ``BGT60LTR11FIFOError`` exception is
        raised. A FIFO overflow occurs if the internal buffer on the
        RadarBaseboardMCU7 is full and old samples had to be discarded.
        In case of a FIFO overflow all samples present in the buffer are
        discarded. If you still need to access them, you can use the
        more low-level method ``get_raw_data``.

        The IFI and IFQ data is between 0 and 1, the average of the signal is
        approximately at 0.5.

        Parameters
        ----------
        num_samples: int
            Number of samples to fetch from the BGT60LTR11.

        Returns
        -------
        ifi: np.array
            IFI data of length `num_samples`.

        ifq: np.array
            IFQ data of length `num_samples`.
        """
        raw_data = np.array([])
        while num_samples > 0:
            n = min(1024, num_samples)
            overflow, data = self.get_raw_data(n)
            if overflow:
                raise BGT60LTR11FIFOError("FIFO overflow")

            # concat vectors
            raw_data = np.hstack([raw_data, data])
            num_samples -= n

        ifq = raw_data[::2]  # Q signal
        ifi = raw_data[1::2]  # I signal

        return ifi, ifq

    def get_configuration(self):
        """Get current device configuration.

        Returns
        -------
        config: dict
            Device configuration.
        """
        config = Bgt60ltr11Config()
        if not c_ltr11_get_configuration(self.handle, byref(config)):
            raise BGT60LTR11Error("Could not get configuration")

        d = {}
        for field in config._fields_:
            d[field[0]] = getattr(config, field[0])
        return d

    def set_configuration(self,
                          mode=0,
                          pulse_width=0,
                          pulse_repetition=1,
                          hold_time=4,
                          detection_threshold=0,
                          tx_power_level=7,
                          rx_if_gain=8,
                          adc=0,
                          sampling_frequency=2000,
                          rf_center_freq=1):
        """Set configuration.

        Parameters
        ----------
        mode: int
          - 0: continuous wave mode
          - 1: pulse mode

        pulse_width: int
            Pulse width. Ignored if mode is continuous wave mode.
            - if chip version = 3 : 
                - 0: 5µs
                - 1: 10µs
                - 2: 3µs
                - 3: 4µs
            - else:
                - 0: 5µs
                - 1: 10µs
                - 2: 20µs
                - 3: 40µs

        pulse_repetition: int
            Pulse repetition. Ignored if mode is continuous wave mode.
              - 0: 250µs
              - 1: 500µs
              - 2: 1000µs
              - 3: 2000µs

        hold_time: int
            - if chip_version = 3 :
                - 0: minimum
                - 1: 500ms
                - 2: 1s
                - 3: 2s
                - 4: 3s
                - 5: 5s
                - 6: 10s
                - 7: 30s
                - 8: 45s
                - 9: 60s
                - 10: 90s
                - 11: 2min
                - 12: 5min
                - 13: 10min
                - 14: 15min
                - 15: 30min
            - else:    
                - 0: 10ms
                - 1: 20ms
                - 2: 40ms
                - 3: 80ms
                - 4: 1s
                - 5: 2s
                - 6: 4s
                - 7: 8s
                - 8: 10s
                - 9: 20s
                - 10: 40s
                - 11: 80s
                - 12: 1min
                - 13: 2min
                - 14: 4min
                - 15: 8min

        detection_threshold: int
            Motion detection threshold. Valid values are [0 ...14]. 
            The lower the value, the higher the motion detection sensitivity.
            

        tx_power_level: int
            Tx power level, the dBm values are preliminary.
              - 0: -34dBm
              - 1: -31.5dBm
              - 2: -25dBm
              - 3: -18dBm
              - 4: -11dBm
              - 5: -5dBm
              - 6: 0dBm
              - 7: 4.5dBm

        rx_if_gain: int
            IF gain.
              - 0: 10dB
              - 1: 15dB
              - 2: 20dB
              - 3: 25dB
              - 4: 30dB
              - 5: 35dB
              - 6: 40dB
              - 7: 45dB
              - 8: 50dB

        adc: int
          - 0: use ADCs of BGT60LTR11
          - 1: use ADCs of RadarBaseboardMCU7

        sampling_frequency: int
            Sampling frequency as integer in Hz (max 3000Hz).  In pulse mode
            this value is ignored and the sampling frequency is given by
            1/pulse_repetition_time (see pulse_repetition).

        rf_center_freq: int 
            RF frequency index as integer. This index corresponds to an RF frequency depending on the pll_japan_mode.

            - Japan mode:
                - 0: 60575MHz
                - 1: 60600MHz
                - 2: 60625MHz
                - 3: 60650MHz
                - 4: 60675MHz
                - 5: 60700MHz
                - 6: 60725MHz
                - 7: 60750MHz
                - 8: 60775MHz
                - 9: 60800MHz
                - 10: 60825MHz
                - 11: 60850MHz
                - 12: 60875MHz
                - 13: 60900MHz
                - 14: 60925MHz

            - Non-Japan mode:
                - 0: 61075MHz
                - 1: 61100MHz
                - 2: 61125MHz
                - 3: 61150MHz
                - 4: 61175MHz
                - 5: 61200MHz
                - 6: 61225MHz
                - 7: 61250MHz
                - 8: 61275MHz
                - 9: 61300MHz
                - 10: 61325MHz
                - 11: 61350MHz
                - 12: 61375MHz
                - 13: 61400MHz
                - 14: 61425MHz

        """
        c = Bgt60ltr11Config(mode,
                             pulse_width,
                             pulse_repetition,
                             hold_time,
                             detection_threshold,
                             tx_power_level,
                             rx_if_gain,
                             adc,
                             sampling_frequency,
                             rf_center_freq)

        if not c_ltr11_set_configuration(self.handle, byref(c)):
            raise BGT60LTR11Error("Could not set configuration")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __del__(self):
        """Destroy device handle"""
        if hasattr(self, "handle") and self.handle:
            c_ltr11_close(self.handle)
            self.handle = None
