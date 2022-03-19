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

# Dependencies:
#   - keyboard: For this script you need keyboard installed.
#     You can install keyboard either using pip:
#         $ pip install keyboard
#     or you use the Anaconda Python distribution
#     https://www.anaconda.com/products/individual

import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import keyboard
import ctypes
from ltr11 import *

class App:
    def __init__(self, master):
        self.master = master

        self.ltr11 = None
        self.init = False
        self.ltr11 = BGT60LTR11()

        #### DEMO CONFIGURATION PARAMETERS, CAN BE CHANGED BY USER ####
        self.mode = 1               # Lock screen: 0, Turn off screen: 1
        self.seconds = 10           # Counter to lock or turn off screen
        self.sensitivity = 7        # Sensitivity between 0:Highest - 15:Lowest
        
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
        master.title("BGT60LTR11AIP Sleep Wakeup Demo")
        master.iconbitmap('demo.ico')
        master.geometry("400x330")
        master.resizable(width=False, height=False)
        master['bg'] = '#FFFFFF'

        # Label for the image
        img = PhotoImage(file='pic_user_absent.png')
        self.label_img = ttk.Label(self.master)
        self.label_img['image'] = img
        img.image = img

        # Label for the detection status
        self.label_det = Label(master,
                               text="...",
                               font=("Source Sans Pro", 12),
                               fg="#644F54",
                               bg="#FFFFFF")

        # Label for the downcounter
        self.label_cnt = Label(master,
                               text="...",
                               font=("Source Sans Pro", 12),
                               fg="#644F54",
                               bg="#FFFFFF")

        self.label_img.pack(side=tk.TOP)
        self.label_det.pack(side=tk.LEFT)
        self.label_cnt.pack(side=tk.RIGHT)

        self.screen_on = True
        self.detected = False

        #### Start  ####
        self._run_demo()

    def __del__(self):
        if self.ltr11:
            if self.init:
                self.ltr11.stop_data_acquisition()

    def _run_demo(self):
        # get detection state
        gpio1, gpio2 = self.ltr11.get_detection()

        if gpio1 == True or gpio2 == True:
            self.detected = True
            self.label_det.configure(text="USER DETECTED", fg="#AB377A")
            self.update_pic('pic_user_present.png')
            self.label_cnt.configure(text="", bg="#FFFFFF")
        else:
            self.detected = False
            self.label_det.configure(text="NO USER DETECTED", fg="#644F54")
            self.update_pic('pic_user_absent.png')
            self.label_cnt.configure(text="%i s" % self.seconds)

        #### MAIN STATE MACHINE ####
        # sleep or wake-up screen based on detection state
        if (self.detected == True) and (self.screen_on == True):
            self.seconds = 10
        elif (self.detected == True) and (self.screen_on == False):
            self.seconds = 10
            # press any keyboard key to wake-up screen
            keyboard.press_and_release('A')
            self.screen_on = True
        elif (self.detected == False) and (self.screen_on == True):
            # start the countdown timer
            self.start_countdown()
            # check if countdown ends
            if self.seconds == 0:  # countdown ends
                if self.mode == 0:
                    # lock screen
                    self.label_cnt.configure(text="Your PC will lock...")
                    self.lock_screen()
                elif self.mode == 1:
                    # turn screen off
                    self.label_cnt.configure(text="Your PC will sleep...")
                    self.turn_screen_off()
                self.screen_on = False
        elif (self.detected == False) and (self.screen_on == False):
            pass

        # request tkinter to call self._run_demo after 1s (the delay is given in ms)
        self.master.after(1000, self._run_demo)

    def start_countdown(self):
        if self.seconds > 0:
            # decrement the time
            self.seconds -= 1
            self.label_cnt.after(5000, self.start_countdown)
        else:
            pass

    def update_pic(self, newpic):
        img = PhotoImage(file=newpic)
        self.label_img['image'] = img
        img.image = img

    def lock_screen(self):
        # lock Windows workstation using LockWorkStation() function from user32.dll
        return ctypes.windll.user32.LockWorkStation()

    def turn_screen_off(self):
        # sleep Windows using SendMessageW() function from user32.dll
        return ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

# main method
if __name__ == '__main__':
    path = os.path.dirname(__file__)
    os.chdir(path)

    root = Tk()
    app = App(root)
    root.mainloop()
