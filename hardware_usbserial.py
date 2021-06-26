# Please do not change this hardware control module for Quisk.
# It provides USB control of RS-HFIQ hardware.
# Updated to work with python3 by 
# Ernesto Perez Estevez - HC6PE <ecualinux@gmail.com>

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
        except Exception as e:
            print(e)
            raise Exception
            
        self.vfo = None

        return None
        
    def open(self): # Called once to open the Hardware
        if serialport.isOpen():
            #Wait for an initial response to verify we're connected
            if DEBUG == 1:
            	print("Attempting handshake with RS-HFIQ using *W command...")
            ver = ''
            attemptCount = 0
            while not ( "HFIQ" in ver ):
                if DEBUG == 1:
                    print("\t...Attempt "+str(attemptCount+1)+".")
                if attemptCount > 10:
                    print("Could not find the RS-HFIQ device. Perhaps wrong usb port ?\nTerminating...")
                    exit()
                attemptCount += 1
                time.sleep(.25)
                serialport.flushInput()
                serialport.flushOutput()
                command='*W\r'
                serialport.write(command.encode())
                ver = serialport.readline().strip().decode()

            if DEBUG == 1:
                print("... Completed handshake with RS-HFIQ.")
            serialport.flushInput()
            serialport.flushOutput()

            # Send init string
            command='*OF2\r'
            serialport.write(command.encode())
            time.sleep(.25)#FIXME: Possibly some sort of race condition requiring this from time to time
            serialport.flush()
            return ver
        else :
            print("Failed to open the RS-HFIO serial port. Perhaps wrong usb port?\nTerminating...")
            exit()

   def close(self): # Called once to close the Hardware
        if serialport.isOpen():
            #Ensure we're not left keyed up and shut off the output level
            cmdstr = '*x0\r*Of0\r'
            serialport.write(cmdstr.encode())
            time.sleep(.25)#FIXME: Possibly some sort of race condition requiring this from time to time
            serialport.flush()
            serialport.close()
        return "Closed"

    def ReturnFrequency(self):
        if serialport.isOpen():
            command='*F?\r'
            serialport.write(command.encode())
            self.current_freq = serialport.readline()
            if DEBUG == 1:
                print("Frequency:", self.current_freq)

        return None, self.current_freq

    def ChangeFrequency(self, tune, vfo, source='', band='', event=None):
        if self.vfo != vfo :
            if serialport.isOpen() :
                self.vfo =vfo 
                vfo_string = '*F' + str(self.vfo) + '\r'
                if DEBUG == 1:
                    print("Tuning to: ", vfo_string)
                print("Tuning to: ", self.vfo)
                serialport.write(vfo_string.encode())

        return tune, self.vfo

    def OnButtonPTT(self, event=None):
      if event:
        if event.GetEventObject().GetValue():
           cmdstr='*x1\r'
           if DEBUG: print('PTT pressed')
        else:
           if DEBUG: print('PTT released')
           cmdstr='*x0\r'
        if serialport.isOpen():
            if DEBUG == 1:
                print("Setting ptt, pttstring:  ", cmdstr)
            serialport.write(cmdstr.encode())
        QS.set_key_down(event.GetEventObject().GetValue())

