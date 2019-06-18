# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 00:04:27 2019

@author: pluu

Contact: tpluu2207 at gmail.com
"""
# =============================================================================
# Reference. LewanSoul Bus Servo Communication Protocol
# http://www.lewansoul.com/download/list/55?page=2
# =============================================================================
# IMPORT PACKAGES
import os, sys, datetime, time
import serial, numpy
import threading
# =============================================================================
# SETTINGS and GLOBAL VARIABLES
SERVO_ID_ALL = 0xfe
CMD_HEADER = 0x55
CMD_MOVE_TIME_WRITE = 1
CMD_MOVE_TIME_READ = 2
CMD_MOVE_TIME_WAIT_WRITE = 7
CMD_MOVE_TIME_WAIT_READ = 8
CMD_MOVE_START = 11
CMD_MOVE_STOP = 12
CMD_ID_WRITE = 13
CMD_ID_READ = 14
CMD_ANGLE_OFFSET_ADJUST = 17
CMD_ANGLE_OFFSET_WRITE = 18
CMD_ANGLE_OFFSET_READ = 19
CMD_ANGLE_LIMIT_WRITE = 20
CMD_ANGLE_LIMIT_READ = 21
CMD_VIN_LIMIT_WRITE = 22
CMD_VIN_LIMIT_READ = 23
CMD_TEMP_MAX_LIMIT_WRITE = 24
CMD_TEMP_MAX_LIMIT_READ = 25
CMD_TEMP_READ = 26
CMD_VIN_READ = 27
CMD_POS_READ = 28
CMD_MOTOR_MODE_WRITE = 29
CMD_MOTOR_MODE_READ = 30
CMD_LOAD_OR_UNLOAD_WRITE = 31
CMD_LOAD_OR_UNLOAD_READ = 32
CMD_LED_CTRL_WRITE = 33
CMD_LED_CTRL_READ = 34
CMD_LED_ERROR_WRITE = 35
CMD_LED_ERROR_READ = 36
CMD_ERROR_OVER_TEMPERATURE = 1
CMD_ERROR_OVER_VOLTAGE = 2
CMD_ERROR_LOCKED_ROTOR = 4
#
WLEN_MOVE_TIME_WRITE = 7
WLEN_MOVE_TIME_READ = 3
WLEN_MOVE_TIME_WAIT_WRITE = 7
WLEN_MOVE_TIME_WAIT_READ = 3
WLEN_MOVE_START = 3
WLEN_MOVE_STOP = 3
WLEN_ID_WRITE = 4
WLEN_ID_READ = 3
WLEN_ANGLE_OFFSET_ADJUST = 4
WLEN_ANGLE_OFFSET_WRITE = 3
WLEN_ANGLE_OFFSET_READ = 3
WLEN_ANGLE_LIMIT_WRITE = 7
WLEN_ANGLE_LIMIT_READ = 3
WLEN_VIN_LIMIT_WRITE = 7
WLEN_VIN_LIMIT_READ = 3
WLEN_TEMP_MAX_LIMIT_WRITE = 4
WLEN_TEMP_MAX_LIMIT_READ = 3
WLEN_TEMP_READ = 3
WLEN_VIN_READ = 3
WLEN_POS_READ = 3
WLEN_MOTOR_MODE_WRITE = 7
WLEN_MOTOR_MODE_READ = 3
WLEN_LOAD_OR_UNLOAD_WRITE = 4
WLEN_LOAD_OR_UNLOAD_READ = 3
WLEN_LED_CTRL_WRITE = 4
WLEN_LED_CTRL_READ = 3
WLEN_LED_ERROR_WRITE = 4
WLEN_LED_ERROR_READ = 3
# =============================================================================
# Length return by read command, Table 4 in the Communication Protocol.
RLEN_MOVE_TIME_READ = 7
RLEN_MOVE_TIME_WAIT_READ = 7
RLEN_ID_READ = 4
RLEN_ANGLE_OFFSET_READ = 4
RLEN_ANGLE_LIMIT_READ = 7
RLEN_VIN_LIMIT_READ = 7
RLEN_TEMP_MAX_LIMIT_READ = 4
RLEN_TEMP_READ = 4
RLEN_VIN_READ = 5
RLEN_POS_READ = 5
RLEN_MOTOR_MODE_READ = 7
RLEN_LOAD_OR_UNLOAD_READ = 4
RLEN_LED_CTRL_READ = 4
RLEN_LED_ERROR_READ = 4
# =============================================================================
# MY PACKAGE
def get_varargin(kwargs, inputkey, defaultValue):
    outputVal = defaultValue
    for key, value in kwargs.items():
        if key == inputkey:
            outputVal = value
        else:
            pass
    return outputVal
# =============================================================================
class servoError(Exception):
    """Base class for exceptions in this module."""
    pass
# =============================================================================
CONTROL_MODE = {0: 'Servo Mode', 1: 'Speed Mode'};

# =============================================================================
class lx16a(object):
    # Initialize    
    def __init__ (self, serialPort, ID):
        self._ID = ID
        self._serial = serialPort;
        self._lock = threading.RLock();
        self._LIMIT_ID = [0, 254];
        self._LIMIT_ANGLE = [0, 240];        
        self._LIMIT_ANGLE_OFFSET = [-30, 30];
        self._LIMIT_SET_ANGLE = [0, 1000];
        self._LIMIT_VIN = [4500, 12000];
        self._LIMIT_TEMP = [50, 100];
        self._LIMIT_SPEED = [-1000, 1000];
        self._LIMIT_SET_TIME = [0, 30000];
        self._angle = self.get_params(param = 'pos', convert = True);
        self._angle_offset = self.get_params(param = 'angle_offset');
        self._vin = self.get_params(param = 'vin', convert = True);
        self._temp = self.get_params(param = 'temp');
        self._speed = self.get_speed();
        self._motor_mode = self.get_params(param = 'motor_mode');
        self._control_mode = self.get_control_mode();
        self._is_load = self.get_params(param = 'load_or_unload');
# =============================================================================
    @property
    def serial(self):
        return self._serial
    @serial.setter
    def serial(self, serialPort):
        self._serial = serialPort;   
    
    @property
    def ID(self):
        return self._ID;
    @ID.setter
    def ID(self, inputVal):
        if lx16a.is_out_of_range(inputVal, self._LIMIT_ID):
            raise servoError('Out of Range. Set ID: {}. Normal range: {}'.format(inputVal,
                            self._LIMIT_ID))
#        Send CMD to modify the parameter
        msg = [CMD_HEADER,CMD_HEADER, self.ID, 
            WLEN_ID_WRITE, CMD_ID_WRITE, inputVal];
        self.sendMsg(msg);
#        Upate Property
        self._ID = inputVal;
        
    @property
    def control_mode(self):
        return self._control_mode;
    @control_mode.setter
    def control_mode(self, inputVal):
        validInput = [0,1];
        if not inputVal in validInput:
            raise servoError('Invalid Input. Set value: {}. Accepted Value: {}'.format(inputVal,
                            validInput))
        self.set_motor_mode(control_mode = inputVal, speed = self.speed);
#        Update Property
        self._control_mode = inputVal;
    
    @property
    def speed(self):
        return self._speed;
    @speed.setter
    def speed(self, inputVal):
        if lx16a.is_out_of_range(inputVal, self._LIMIT_SPEED):
            raise servoError('Out of Range. Set Speed: {}. Normal range: {}'.format(inputVal,
                            self._LIMIT_SPEED))
        self.set_motor_mode(control_mode = self.control_mode, speed = inputVal)
        self._speed = inputVal; 
        
    @property
    def angle(self):   
        self._angle = self.get_params(param = 'pos', convert = True);
        return self._angle;
    @angle.setter
    def angle(self, inputVal):
        if lx16a.is_out_of_range(inputVal, self._LIMIT_ANGLE):
            raise servoError('Out of Range. Set angle: {}. Normal range: {}'.format(inputVal,
                            self._LIMIT_ANGLE))
        self._angle = inputVal;
        
    @property
    def angle_offset(self):
        return self._angle_offset;
    @angle_offset.setter
    def angle_offset(self, inputVal):
        if lx16a.is_out_of_range(inputVal, self._LIMIT_ANGLE_OFFSET):
            raise servoError('Out of Range. Set offset angle: {}. Normal range: {}'.format(inputVal,
                            self._LIMIT_ANGLE_OFFSET))
#        Send CMD to modify the parameter
        setVal = int(lx16a.linMap(inputVal,self._LIMIT_ANGLE_OFFSET,[-125, 125]));
        if setVal < 0 : setVal += 256;
        print(setVal)
        msg = [CMD_HEADER,CMD_HEADER, self.ID, 
            WLEN_ANGLE_OFFSET_ADJUST, CMD_ANGLE_OFFSET_ADJUST, setVal];
        self.sendMsg(msg);        
#        Upate Property
        self._angle_offset = inputVal;
        
    @property
    def vin(self):
        return self._vin;
    @vin.setter
    def vin(self, inputVal):
        if lx16a.is_out_of_range(inputVal, self._LIMIT_VIN):
            raise servoError('Out of Range. Set Input Voltage: {}. Normal range: {}'.format(inputVal,
                            self._LIMIT_VIN))
        self._vin = inputVal;
        
    @property
    def temp(self):
        return self._temp
    
    @property
    def is_load(self):
#        self._is_load = self.get_params(param = 'load_or_unload')
        return self._is_load
    
    @property
    def motor_mode(self):
        return self._motor_mode;
    @motor_mode.setter
    def motor_mode(self, inputVal):
        self._motor_mode = inputVal;
        
    def show_motor_status(self):
        print('LX16A Servo Motor Status:')
        print('\t Motor ID: {}'.format(self.ID))
        print('\t Angle: {} Deg'.format(self.angle))
        print('\t Angle Offset: {} Deg'.format(self.angle_offset))
        print('\t Vin: {} V'.format(self.vin))
        print('\t Temperature: {}'.format(self.temp))
        print('\t Speed: {}'.format(self.speed))
        print('\t Motor Mode: {}'.format(self.motor_mode))
        print('\t Control Mode: {}-{}'.format(self.control_mode,
            CONTROL_MODE[self.control_mode]))
        print('\t Running: {}'.format(self.is_load))
        
# =============================================================================
    
# =============================================================================
# METHODS
# =============================================================================
    def sendMsg(self,cmdstr, **kwargs):
        param = get_varargin(kwargs, 'param',None);
        cmd, wlen, rlen = lx16a.get_cmd_code(cmdstr);
        msg = [CMD_HEADER,CMD_HEADER, self.ID, wlen, cmd];
        if param is None:
            pass;
        else:
            for byteVal in param:
                msg.append(byteVal);
        msg.append(lx16a.checksum(msg));
        msg = bytes(msg)
        with self._lock:
            self.serial.write(msg)
# =============================================================================
    def get_params(self, **kwargs):
        param = get_varargin(kwargs, 'param', 'id');
        convert = get_varargin(kwargs, 'convert', False);
        cmdstr = param.upper() + '_READ';
        cmd, wlen, rlen = lx16a.get_cmd_code(cmdstr);
        rlen_param = rlen - wlen
        self.sendMsg(cmdstr)
        returned_Bytes = []
        for i in range(rlen + 3):
            returned_Bytes.append(self.serial.read())
            
        returned_Bytes = [int.from_bytes(b, byteorder="little") for b in returned_Bytes]
        lx16a.checkMsg(returned_Bytes)
        val_Bytes = returned_Bytes[wlen+2:wlen+2+rlen_param];
        returned_val = val_Bytes;
        if convert is True:
            if param == 'pos':
                int_val = lx16a.word(val_Bytes)
                if int_val > 2**15:
                    int_val -= 2**16
#                returned_val = float(lx16a.linMap(int_val,[-1000, 1000], self._LIMIT_ANGLE))
                returned_val = int_val
            elif param == 'vin':
                returned_val = float(lx16a.word(val_Bytes)/1000)
            else:
                pass
        return returned_val
# =============================================================================
    def get_speed(self):
        motor_mode = self.get_params(param = 'motor_mode');
        speed = lx16a.word(motor_mode[2:4])
        if speed > 2**15:
            speed -= 2**16    
        return speed
# =============================================================================
    def get_control_mode(self):
        motor_mode = self.get_params(param = 'motor_mode');
        return motor_mode[0]
# =============================================================================
# SET PARAMETERS
# =============================================================================          
    def set_motor_mode(self, **kwargs):
        control_mode = get_varargin(kwargs, 'control_mode', 0);
#        0: Servo mode or Position control mode.
#        1: Motor mode or Speed control mode.
        speed = get_varargin(kwargs, 'speed', 0);
        if speed < 0:
            speed += 2**16        
#        msg = [CMD_HEADER,CMD_HEADER, self.ID, 
#           WLEN_MOTOR_MODE_WRITE, CMD_MOTOR_MODE_WRITE,
#           control_mode, 0, lx16a.lowByte(speed), lx16a.highByte(speed)];
#        self.sendMsg(msg);
        self.sendMsg('MOTOR_MODE_WRITE', 
                    param = [control_mode, 0,
                            lx16a.lowByte(speed), lx16a.highByte(speed)])
# =============================================================================
    def set_position(self, angle):
#        set_angle = lx16a.linMap(angle, self._LIMIT_ANGLE, self._LIMIT_SET_ANGLE)
#        set_angle = lx16a.threshold(set_angle, self._LIMIT_SET_ANGLE);
#        set_time = lx16a.threshold(set_angle/self.speed, self._LIMIT_SET_TIME)        
        set_angle = int(angle)
        print(set_angle)
        set_time = 0;
#        msg = [CMD_HEADER,CMD_HEADER, self.ID, 
#           WLEN_MOVE_TIME_WRITE, CMD_MOVE_TIME_WRITE,
#           lx16a.lowByte(set_angle), lx16a.highByte(set_angle),
#           lx16a.lowByte(set_time), lx16a.highByte(set_time)];
#        self.sendMsg(msg);
        self.sendMsg('MOVE_TIME_WRITE',
                    param = [lx16a.lowByte(set_angle), lx16a.highByte(set_angle),
                            lx16a.lowByte(set_time), lx16a.highByte(set_time)])
# =============================================================================

# =============================================================================
# STATIC METHODS
# =============================================================================
    @staticmethod
    def checkMsg(msg):
        if lx16a.checksum(msg[:-1]) != msg[-1]:
            print("Invalid checksum")
# =============================================================================
    @staticmethod
    def get_cmd_code(cmdstr):
        cmd = None;
        wlen = None;
        rlen = None;
        _locals = locals();
        exec('cmd = CMD_%s'%(cmdstr), globals(), _locals)
        cmd = _locals['cmd']
        exec('wlen = WLEN_%s' % (cmdstr), globals(), _locals);
        wlen = _locals['wlen']
        try:
            exec('rlen = RLEN_%s' % (cmdstr), globals(), _locals);
            rlen = _locals['rlen']
        except:
            pass;
        return cmd, wlen, rlen
# =============================================================================
    @staticmethod
    def lowByte(value):
        return int(value) % 256
# =============================================================================
    def highByte(value):
        return int(value // 256)
# =============================================================================
    def checksum(msg):
#      Checksum:The calculation method is as follows:
#      Checksum=~(ID+ Length+Cmd+ Prm1+...PrmN)If the numbers in the
#      brackets are calculated and exceeded 255,Then take the lowest one byte, "~" means Negation.
        check = ~sum(msg[2:])
        return check & 255
# =============================================================================
    @staticmethod
    def toBytes(value):        
#       Convert two byte int value into high and low byte
        return([int(value) >> 8, int(value) & 0x00ff])
# =============================================================================
    @staticmethod
    def bytes_to_Val(twoBytes, outRange):
        int_val = lx16a.word(twoBytes[0], twoBytes[1]);
        return lx16a.linMap(int_val, [0, 65535], outRange);
# =============================================================================
    @staticmethod
    def word(twoBytes):
        low = twoBytes[0];
        high = twoBytes[1];
        return int(low) + int(high)*256
# =============================================================================
    @staticmethod
    def is_out_of_range(val, rangeVal):
        if val < rangeVal[0] or val > rangeVal[1]:
            return True
        else:
            return False    
# =============================================================================
    @staticmethod
    def linMap(inputVal, inRange, outRange):
        outputVal = (outRange[1]-outRange[0])*(inputVal-inRange[0])/(inRange[1]-inRange[0]) + outRange[0];
        return outputVal
# =============================================================================
    @staticmethod
    def threshold(value, inputRange):
        range_min = inputRange[0];
        range_max = inputRange[1];
        return min(range_max, max(range_min, value))
# =============================================================================
# MAIN
from math import sin
def main():
    print(lx16a.get_cmd_code('ID_WRITE'))
#    print(cmd, wlen, rlen)
    serialPort = serial.Serial('COM7', 115200, timeout = 2)
    servo = lx16a(serialPort, 1)    
    servo.show_motor_status()
    servo.control_mode = 0;
#    servo.speed = 200;    
#    servo.set_position(240)
    servo.control_mode
    print(servo.angle)
    t = 0;
    try:
        while True:
            pos = lx16a.linMap(sin(t)*120+120, [0, 240], [0,1000]);
            servo.set_position(pos)
            t += 0.01
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('Exit')
# =============================================================================
# DEBUG
if __name__ == '__main__':    
    main()
    