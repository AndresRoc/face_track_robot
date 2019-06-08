# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:24:31 2019

@author: pluu
"""

import serial
BAUDRATE = 115200;
PORT = 'COM9';
mySerial = serial.Serial(PORT, BAUDRATE, timeout = 1);
if not mySerial.is_open:
    mySerial.open()    
else:
    mySerial.write(("pyserial test\n").encode())
    print('closing serial port');
    mySerial.close();