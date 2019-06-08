# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:17:34 2019

@author: pluu

Contact: tpluu2207 at gmail.com
"""
# =============================================================================
# IMPORT PACKAGES
import os, sys, datetime, logging
import serial
import time
from lewansoul_lx16a_controller import ServoController
# =============================================================================
# SETTINGS and GLOBAL VARIABLES
LOGGER = logging.getLogger('lewansoul.servos.lx16a')
mySerial = serial.Serial('COM7', 115200, timeout=2)
if not mySerial.is_open:
    mySerial.open()    
# =============================================================================
# MY PACKAGE
sys.path.append('G:\OneDrive\luuPyCode')
from luu_utils import get_varargin
# =============================================================================
def checksum(packet):
	s = ~sum(packet[2:])
	return s & 255
# =============================================================================
def sendPacket(packet):
    packet.append(checksum(packet))
    packet = bytes(packet)
    mySerial.write(packet)
# =============================================================================
def checkPacket(packet):
    if checksum(packet[:-1]) != packet[-1]:
        print("Invalid checksum")    
        
def IDRead():
    packet = [0x55, 0x55, 1, 3, 14]
    sendPacket(packet)
    returned = []
    print('Read ID')
    for i in range(7):
        returned.append(mySerial.read())
    print(returned)
		
    returned = [int.from_bytes(b, byteorder="little") for b in returned]
    checkPacket(returned)
		
    data = returned[5]
		
    return data        
# =============================================================================
def hex_data(data):
    return '[%s]' % ', '.join(['0x%02x' % x for x in data])    
# MAIN
def main():
    logging.basicConfig(level=logging.DEBUG)
    print(IDRead())
#    else:
#    mySerial.write(("pyserial test\n").encode())
#        print('closing serial port');
#        mySerial.close();
#    c = ServoController(mySerial, timeout=8)
#    
#    print(c.get_battery_voltage())
#    
#    servo1_id = 1
#    
#    print(c.get_positions([servo1_id]))
#    
#    c.move({servo1_id: 1000}, time=300)
#    time.sleep(0.3)
#    c.move({servo1_id: 800}, time=2000)
#    time.sleep(2)
#    c.unload([servo1_id])
#    time.sleep(0.1) # important not to close serial connection immediately
# =============================================================================
# DEBUG
if __name__ == '__main__':
    main()
