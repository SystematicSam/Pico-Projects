# A basic class to use the Makerverse RV3028 Supercap Real Time Clock on the Raspberry Pi Pico
# Written by Brenton Schulz, Peter Johnston and Michael Ruppe at Core Electronics
# 2022 May 18  Add alarm functions - MR
# 2022 May 4th Use class attributes instead of setters/getters
# 2021 NOV 5th Initial feature set complete
#     - Set / get date and time
#     - Set / get UNIX time (independent of main calendar clock)
#     - Enable event interrupt on EVI pin
#     - Get event timestamp
#     - Configure trickle charger for onboard supercap
#     - Configure frequency of CLK output pin

from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_dayNames=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
_I2C_ADDRESS = 0x52
_SEC = 0x00
_MIN = 0x01
_HOUR = 0x02
_DAY = 0x04
_MONTH = 0x05
_YEAR = 0x06
_ALMIN = 0x07
_STATUS = 0x0E
_CTRL1 = 0x0F
_CTRL2 = 0x10
_CIM = 0x12
_ECTRL = 0x13
_SECTS = 0x15
_DAYTS = 0x18
_UNIX = 0x1B
_REG_ID = 0x28
_EE_CLKOUT = 0x35
_EE_BACKUP = 0x37

def _setBit(x, n):
    return x | (1 << n)

def _clearBit(x, n):
    return x & ~(1 << n)

def _writeBit(x, n, b):
    if b == 0:
        return _clearBit(x, n)
    else:
        return _setBit(x, n)
    
def _readBit(x, n):
    return x & 1 << n != 0
    
def _writeCrumb(x, n, c):
    x = _writeBit(x, n, _readBit(c, 0))
    return _writeBit(x, n+1, _readBit(c, 1))

def _writeTribit(x,n,c):
    x = _writeBit(x, n, _readBit(c, 0))
    x = _writeBit(x, n+1, _readBit(c, 1))
    return _writeBit(x, n+2, _readBit(c, 2)) 

def _bcdDecode(val):
    return (val>>4)*10 + (val&0x0F)

def _bcdEncode(val):
    return ((val//10) << 4) | (val % 10)

class PiicoDev_RV3028(object):    
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=_I2C_ADDRESS):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)

        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
 
        try:
            part = int(self.i2c.readfrom_mem(self.addr, _REG_ID, 1)[0])
        except Exception as e:
            print(i2c_err_str.format(self.addr))
            raise e
        
        self._weekday = 0 # integer 0 to 6
        self.alarmHours=0
        self.alarm_ampm='am' # for defining alam AM/PM. Ignored if system time is 24-hr
        self.alarmMinutes=0
        self.alarmWeekdayDate=0
        self.setBatterySwitchover()
        self.configTrickleCharger()
        self.setTrickleCharger()
        self.getDateTime()
        
    @property
    def weekday(self):
        """Get the weekday and return as integer 0 to 6"""
        return self._weekday
    @weekday.setter
    def weekday(self, day):
        """Set the weekday. Accepts an integer 0 to 6"""
        if 0 <= day <= 6: self._weekday = day
        else: print('Warning: Weekday must be integer 0 to 6')
    
    @property
    def weekdayName(self):
        """Get the weekday and return as a string."""
        return _dayNames[self._weekday]
    @weekdayName.setter
    def weekdayName(self, day):
        """Set the weekday. Accepts a string, checks string is a day name, and stores as integer 0 to 6"""
        if day in _dayNames: self._weekday = _dayNames.index(day)
        else: print('Warning: weekdayName must be "Monday", "Tuesday", ... "Saturday" or "Sunday"')

    def _read(self, reg, N):
        try:
            tmp = int.from_bytes(self.i2c.readfrom_mem(self.addr, reg, N), 'little')
        except:
            print("Error reading from RV3028")
            return float('NaN')
        return tmp
        
    def _write(self, reg, data):
        try:
            self.i2c.writeto_mem(self.addr, reg, data)
        except:
            print("Error writing to RV3028")
            return float('NaN')
        
    def getUnixTime(self):
        return self._read(_UNIX, 4)
    
    def setUnixTime(self, time):
        self._write(_UNIX, time.to_bytes(4, 'little'))
        
    def setBatterySwitchover(self, state = True):
        tmp = self._read(_EE_BACKUP, 1)
        if state is True:
            tmp = _writeCrumb(tmp, 2, 0b01