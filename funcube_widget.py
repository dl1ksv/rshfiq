# This module is used to add LNA and Mixer gain widget to the QUISK screen.

from __future__ import print_function

import math, wx

class BottomWidgets:    # Add extra widgets to the bottom of the screen
  def __init__(self, app, hardware, conf, frame, gbs, vertBox):
    self.config = conf
    self.hardware = hardware
    self.application = app
    self.start_row = app.widget_row                     # The first available row
    self.start_col = app.button_start_col       # The start of the button columns
    
    self.Widgets_0x06(app, hardware, conf, frame, gbs, vertBox)

  def Widgets_0x06(self, app, hardware, conf, frame, gbs, vertBox):
    self.num_rows_added = 1
    start_row = self.start_row

    lna = app.QuiskCheckbutton(frame, self.OnLNA, 'LNA')
    lna.SetValue( self.hardware.lna )
    gbs.Add(lna, (start_row, self.start_col), (1, 2), flag=wx.EXPAND)

    mixer = app.QuiskCheckbutton(frame, self.OnMixer, 'Mixer gain')
    mixer.SetValue( self.hardware.mixer )
    gbs.Add(mixer, (start_row, self.start_col+2), (1, 2), flag=wx.EXPAND)
  
    gain = app.SliderBoxHH(frame, 'If gain %d dB', 0, 0, 59, self.OnIF, True)
    gain.SetValue(self.hardware.ifgain)
    gbs.Add(gain,(start_row, self.start_col+4),(1,4), flag=wx.EXPAND)

  def OnLNA(self, event):
    btn = event.GetEventObject()
    if btn.GetValue() :
	value = 1
    else :
	value = 0
    print('LNA: ',value)
    self.hardware.SetLNA(value)

  def OnMixer(self, event):
    btn = event.GetEventObject()
    if btn.GetValue() :
	value = 1
    else :
	value = 0
    print('Mixer: ',value)
    self.hardware.SetMixer(value)

  def OnIF(self,event) :
    btn = event.GetEventObject()
    value = btn.GetValue()
    print('IF: ', value )
    self.hardware.SetIfGain(value)

