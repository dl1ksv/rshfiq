# Please do not change this hardware control module for Quisk.
# It provides USB / serial control of RS-HFIQ hardware.

from __future__ import print_function

import struct, threading, time, traceback, math
from quisk_hardware_model import Hardware as BaseHardware
import _quisk as QS

import Hamlib

DEBUG = 0

class Hardware(BaseHardware):
    def __init__(self, app, conf):
        BaseHardware.__init__(self, app, conf)
        self.model=25019			#Could be a paramter later, to handel different models
        self.vfo = None
        self.receiver = Hamlib.Rig(self.model)
        self.receiver.state.rigport.pathname='/dev/ttyUSB0' #Could be a parameter later

    def open(self):
        ret = BaseHardware.open(self)	# Called once to open the Hardware
        #if not (self.receiver.open() == Hamlib.RIG_OK) :
        #     print("Could not open rig 2519: ",self.receiver.caps.model_name)
        #     return 'Error'
        self.receiver.open()
        self.vfo = int(self.receiver.get_freq())
        return ret

    def close(self):			# Called once to close the Hardware
        self.receiver.close()

    def ReturnFrequency(self):
        if DEBUG == 1:
             print("Frequency:", self.vfo)

        return None, self.vfo

    def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
        if self.vfo != vfo :
            self.receiver.set_freq(Hamlib.RIG_VFO_CURR,vfo)
            self.vfo = vfo
            if DEBUG == 1:
                print("Tuning to: ", self.vfo)

        return tune, self.vfo
    def OnButtonPTT(self, event=None):
        self.ptt_button=0
        if event:
            if event.GetEventObject().GetValue():
                self.ptt_button = 1
                if DEBUG: print('PTT pressed')
            else:
                if DEBUG: print('PTT released')
                self.ptt_button = 0

        self.receiver.set_ptt(Hamlib.RIG_VFO_CURR,self.ptt_button)
        QS.set_key_down(self.ptt_button)

 
