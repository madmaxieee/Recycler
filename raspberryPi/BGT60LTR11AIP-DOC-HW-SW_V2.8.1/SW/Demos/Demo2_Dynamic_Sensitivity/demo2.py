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

import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import time
from ltr11 import *

class App:
    def __init__(self, master):
        self.master = master

        self.ltr11 = None
        self.init = False
        self.ltr11 = BGT60LTR11()

        #### DEMO CONFIGURATION PARAMETERS, CAN BE CHANGED BY USER ####
        self.time_short_range = 2
        self.wait_time = 3          # Time without target detection (in seconds)
        self.sensitivity = 0        # Sensitivity between 0:MAX - 15:MIN

        self.ltr11.set_configuration(mode=1,
                                     pulse_width=0,
                                     pulse_repetition=1,
                                     hold_time=4,
                                     detection_threshold=self.sensitivity,
                                     tx_power_level=7,
                                     rx_if_gain=8,
                                     adc=1,
                                     sampling_frequency=2000)

        #### Create GUI Elements ###########
        master.title("BGT60LTR11AIP Dynamic Sensitivity Demo")
        master.iconbitmap('demo.ico')
        master.geometry("400x330")
        master.resizable(width=False, height=False)
        master['bg'] = '#FFFFFF'

        # Label for the image
        img = PhotoImage(file='pic_no_det.png')
        self.label_img = ttk.Label(self.master)
        self.label_img['image'] = img
        img.image = img

        # Label for the detection status
        self.label_det = Label(master,
                               text="...",
                               font=("Source Sans Pro", 12),
                               fg="#AB377A",
                               bg="#FFFFFF")

        # Label for the sensitivity status
        self.label_sen = Label(master,
                               text="...",
                               font=("Source Sans Pro", 12),
                               fg="#644F54",
                               bg="#FFFFFF")

        # Label for the downcounter
        self.label_tim = Label(master,
                               text="...",
                               font=("Source Sans Pro", 12),
                               fg="#644F54",
                               bg="#FFFFFF")

        self.label_img.pack(side=tk.TOP)
        self.label_det.pack(side=tk.LEFT)
        self.label_sen.pack(side=tk.LEFT)
        self.label_tim.pack(side=tk.RIGHT)

        self.state = True  # long range
        self.ltr11.start_data_acquisition()
        self.init = True
        # Flag to control target
        # If there is no target after 3seconds go back to initial state
        self.flag_to_back = False
        self.start_time = time.time()

        #### Start  ####
        self.running = True
        self._run_demo()

    def __del__(self):
        if self.ltr11:
            if self.init:
                self.ltr11.stop_data_acquisition()

    def _run_demo(self):
        gpio1, gpio2 = self.ltr11.get_detection()

        if self.running:
            if gpio1:
                self.time_short_range = time.time()
                # Target detected in low sensitivity
                # change sensitivity to MIN, to check if the target is in shorter range
                if self.state:
                    self.label_det.configure(text="FAR TARGET DETECTED ")
                    self.update_pic('pic_far_det.png')
                    self.sensitivity = 15
                    self.change_sensitivity()
                    self.label_sen.configure(text="SENSITIVITY: MIN")
                    self.flag_to_back = True
                    self.state = False  # short range state
                # Show that the target is detected in shorter range
                else:
                    self.label_det.configure(text="CLOSE TARGET DETECTED ")
                    self.update_pic('pic_close_det.png')
            # after 3 sec without target detection, go back to initial state MAX Sensitivity
            if self.flag_to_back:
                if time.time() - self.time_short_range > self.wait_time:
                    self.sensitivity = 0
                    self.change_sensitivity()
                    self.label_sen.configure(text="SENSITIVITY: MAX")
                    self.flag_to_back = False
                    self.state = True  # longer range state
                else:
                    self.label_tim.configure(text="%.1f s" % (
                        time.time() - self.time_short_range))

        self.master.after(100, self._run_demo)

    def update_pic(self, newpic):
        img = PhotoImage(file=newpic)
        self.label_img['image'] = img
        img.image = img

    def change_sensitivity(self):
        self.ltr11.soft_reset()
        # reconfigure with new sensitivity
        self.ltr11.set_configuration(mode=1,
                                     pulse_width=0,
                                     pulse_repetition=1,
                                     hold_time=4,
                                     detection_threshold=self.sensitivity,
                                     tx_power_level=7,
                                     rx_if_gain=8,
                                     adc=1,
                                     sampling_frequency=2000)
        self.ltr11.start_data_acquisition()
        self.init = True

# main method
if __name__ == '__main__':
    path = os.path.dirname(__file__)
    os.chdir(path)

    root = Tk()
    app = App(root)
    root.mainloop()
