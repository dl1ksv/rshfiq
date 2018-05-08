# Please do not change this hardware control module for Quisk.
# It provides USB / serial control of FuncubePro+ hardware.

from __future__ import print_function

import struct, threading, time, traceback, math
from quisk_hardware_model import Hardware as BaseHardware
import _quisk as QS

import Hamlib

DEBUG = 1

class Hardware(BaseHardware):
    def __init__(self, app, conf):
        BaseHardware.__init__(self, app, conf)
	self.model=2518			# Funcube Pro+
        self.vfo = None
	self.lna = None
	self.mixer = None
	self.ifgain = None
	self.receiver = Hamlib.Rig(self.model)
	self.receiver.open()
        self.vfo = int(self.receiver.get_freq())
	if(self.vfo == 0 ):
	       print('+++ Could not find FuncubePro+ !\nExiting')
	       exit()	
	
	self.mixer = self.receiver.get_level_i(Hamlib.RIG_LEVEL_ATT,Hamlib.RIG_VFO_CURR)
	self.lna = self.receiver.get_level_i(Hamlib.RIG_LEVEL_PREAMP,Hamlib.RIG_VFO_CURR)
        self.ifgain = (int)(self.receiver.get_level_f(Hamlib.RIG_LEVEL_RF,Hamlib.RIG_VFO_CURR)*100)

    def open(self):
	ret = BaseHardware.open(self)	# Called once to open the Hardware

        if DEBUG == 1 :
            print('Device opened')
        return ret

    def close(self):			# Called once to close the Hardware
        self.receiver.close()

    def ReturnFrequency(self):
        #if DEBUG == 1:
        #     print("Frequency:", self.vfo)

        return None, self.vfo

    def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
        if self.vfo <> vfo :
	     self.receiver.set_freq(Hamlib.RIG_VFO_CURR,vfo)
             self.vfo = vfo
             if DEBUG == 1:
            	print("Tuning to: ", self.vfo)

        return tune, self.vfo

    def SetLNA(self,level):
 	if level != self.lna:
		ret=self.receiver.set_level(Hamlib.RIG_LEVEL_PREAMP,level,Hamlib.RIG_VFO_CURR)
		self.lna = level
    
    def GetLNA(self):
	return self.lna
 
    def SetMixer(self,level):
 	if level != self.mixer:
		ret=self.receiver.set_level(Hamlib.RIG_LEVEL_ATT,level,Hamlib.RIG_VFO_CURR)
		self.mixer = level
    
    def GetMixer(self):
	return self.mixer

    def GetIfGain(self) :
	return self.ifgain

    def SetIfGain(self, level) :
  	if level != self.ifgain:
		ret=self.receiver.set_level(Hamlib.RIG_LEVEL_RF,(float)(level)/100.,Hamlib.RIG_VFO_CURR)
		self.ifgain = level
 
