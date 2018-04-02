rshfiq serves has hardware description of the RS-HFIQ from HobbyPCB to be used with quisk.

This package was tested with quisk-4.1.14  and wsjtx in WSPR mode. It should work with older versions of quisk, too.

It contains two possible hardware descriptions: 

  * hardware_usbserial.py
  
    This description requires the pyserial package. Using this descriptions quisk directly communicates with the rs-hfiq hardware via the serialport, normally /dev/ttyUSB0.
 If your system uses another port, you have to modify

    serialport.port = "/dev/ttyUSB0"
accordingly.
 

  * hardware_rshfiq_hamlib.py
    This description requires hamlib with python bindings.
    This description may be adopted to other models supported by hamlib, for instance the funcube dongle.

 
If you have a running installation of quisk, untar or clone this repository. Then start quisk and select config.

Select the 'Radios' tab, select 'Add a new radio'. I suggest to choose Softrock fixed. After adding choose the tab of the new created radio  and switch to the Hardware tab.

Here select the hardware_usbserial.py. 

Then do the sond device settings depending on your configuration.

**Important:**
On my system I had to change the I/Q channels for I/Q Sample Input and Tx Output.

With some soundcards I got no sound on transmit.
The solution was to use

plughw:x,y instead of the hw:x,y proposed by quisk.

