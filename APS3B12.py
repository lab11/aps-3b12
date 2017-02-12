
import serial
import time
import sys


class APS3B12(object):

    def serial_write_byte_UTF8(self, text):
        self.serial.write(text.encode(encoding="utf-8"))
        time.sleep(.03)

    def load_enable(self, enable, verbose):
        # remote only mode
        self.serial_write_byte_UTF8('REM;')
        if enable:
            if(verbose):
                print('Enabling load')
            self.serial_write_byte_UTF8('LOAD 1;')
            self.state = True
        else:
            if(verbose):
                print('Disabling load')
            self.serial_write_byte_UTF8('CC:A 0;')
            self.serial_write_byte_UTF8('LOAD 0;')
            self.state = False
        # local only mode
        self.serial_write_byte_UTF8('LOC;')

    def __init__(self, dev, reset):
        try:
            self.serial = serial.Serial(dev, 9600)
        except:
            sys.exit('Cannot find {:}'.format(dev))
        if reset:
            self.load_enable(False)
            self.set_get_bank_wave('SET', 'BANK', 0)
            self.set_get_bank_wave('SET', 'WAVE', 0)
        # maximum current setting
        self.MAX_CURRENT_SETTING = 10

    def get_loadState(self):
        # remote only mode
        self.serial_write_byte_UTF8('REM;')
        self.serial_write_byte_UTF8('LOAD?')
        state = int(self.serial.read(1).decode(encoding='utf-8').rstrip())
        print('Load state: {:}'.format(state))
        # local only mode
        self.serial_write_byte_UTF8('LOC;')
        return True if state else False
    
    def get_value(self, measType):
        # remote only mode
        self.serial_write_byte_UTF8('REM;')
        if measType == 'I':
            self.serial_write_byte_UTF8('MEAS:CURR?;')
        elif measType == 'V':
            self.serial_write_byte_UTF8('MEAS:VOLT?;')
        elif measType == 'W':
            self.serial_write_byte_UTF8('MEAS:POW?;')
        value = self.serial.read(8).decode(encoding='utf-8')
        value = float(value.strip())
        ## local only mode
        self.serial_write_byte_UTF8('LOC;')
        return value
    
    def set_value(self, valType, value, verbose):
        if not self.state:
            print("Load not enabled, command ignored")
            return -1
        # remote only mode
        self.serial_write_byte_UTF8('REM;')
        value = float(value)
        if valType == 'I' and value >= 0 and value <= self.MAX_CURRENT_SETTING:
            self.serial_write_byte_UTF8('CC:A ' + str(value) + ';')
            if(verbose):
                print('Setting current to {:.3f} (A)'.format(value))
        elif valType == 'W':
            if(verbose):
                print("Setting wattage to {:.3f} (W)".format(value))
                print("Please wait for command to finish")
            v_meas = self.get_value('V')
            i = value/v_meas if v_meas > 0 else value/120
            self.set_value('I', i)
            time.sleep(1)
            p_meas = self.get_value('W')
            # v_meas <= 120, actual current should be higher than calcualted
            if p_meas > 0:
                i *= value/p_meas
                self.set_value('I', i)
        # local only mode
        self.serial_write_byte_UTF8('LOC;')
        time.sleep(1)
        return self.get_value(valType)

    def set_get_bank_wave(self, set_get, valType, value):
        if valType == 'BANK' or valType == 'WAVE':
            if set_get == 'SET':
                value = int(value)
                upperLim = 10 if valType == 'BANK' else 4
                if value < 0 or value > upperLim:
                    print('invalid input value, 0 <= ' + valType + ' <= ' + str(uppLim))
                    return
            # remote only mode
            self.serial_write_byte_UTF8('REM;')
            if set_get == 'SET':
                self.serial_write_byte_UTF8(valType + ' ' + str(value) + ';')
            else:
                self.serial_write_byte_UTF8(valType + ' ?;')
                tmp = self.serial.read(4).decode(encoding='utf-8')
                tmp = int(tmp.strip())
            # local only mode
            self.serial_write_byte_UTF8('LOC;')
            if set_get == 'GET':
                return tmp
        else:
            print('Invalid type')

