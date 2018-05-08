# Please do not change this hardware control module for Quisk.
# It provides USB control of RS-HFIQ hardware.

from __future__ import print_function

import struct, threading, time, traceback, math

from quisk_hardware_model import Hardware as BaseHardware
import _quisk as QS

import serial

DEBUG = 0

serialport = serial.Serial()

class Hardware(BaseHardware):
    def __init__(self, app, conf):
        BaseHardware.__init__(self, app, conf)

        # Default port settings for RS-HFIQ

        serialport.port = "/dev/ttyUSB0"
        serialport.baudrate = 57600
        serialport.bytesize = serial.EIGHTBITS #number of bits per bytes
        serialport.parity = serial.PARITY_NONE #set parity check: no parity
        serialport.stopbits = serial.STOPBITS_ONE #number of stop bits
        serialport.timeout = 1            #non-block read
	serialport.rtscts = False
	
        try:
            serialport.open()
        except Exception, e:
            print(e)
            raise Exception

        if serialport.isOpen():

            serialport.flushInput() #flush input buffer, discarding all its contents
            serialport.flushOutput()#flush output buffer, aborting current output
            #and discard all that is in buffer

            # Send init string
            #print("Sending init string")
            #serialport.write("*OF2\r")

            # Wait a moment for init to finish
            time.sleep(1)

        self.vfo = None

        return None
    def open(self):			# Called once to open the Hardware
        if serialport.isOpen():
            # Get RS-HFIQ version string
            serialport.write("*W\r")
            text = serialport.readline()
            print("Retrieved version: ", text)
	    if text[0:7] == "RS-HFIQ" :
        	return text
	    else :
		print("Could not find the RS-HFIQ device. Perhaps wrong usb port ?\nTerminating")
		exit()
    def close(self):			# Called once to close the Hardware

        if serialport.isOpen():
            serialport.close()

        return "Closed"

    def ReturnFrequency(self):
        if serialport.isOpen():
            serialport.write("*F?\r")
            self.current_freq = serialport.readline()
            if DEBUG == 1:
                print("Frequency:", self.current_freq)

        return None, self.current_freq

    def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
        if self.vfo <> vfo :
            if serialport.isOpen() :
                self.vfo =vfo 
                vfo_string = "*F" + str(self.vfo) + "\r"
                if DEBUG == 1:
                    print("Tuning to: ", vfo_string)
                print("Tuning to: ", self.vfo)
                serialport.write(vfo_string)

        return tune, self.vfo

    def OnButtonPTT(self, event=None):
      if event:
        if event.GetEventObject().GetValue():
           cmdstr="*x1\r"
           if DEBUG: print('PTT pressed')
        else:
           if DEBUG: print('PTT released')
           cmdstr="*x0\r"
        if serialport.isOpen():
            if DEBUG == 1:
                print("Setting ptt, pttstring:  ", cmdstr)
            serialport.write(cmdstr)
        QS.set_key_down(event.GetEventObject().GetValue())

 
