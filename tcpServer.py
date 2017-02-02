
#! /usr/bin/python3
import APS3B12

import socket
import sys

DEV = '/dev/ttyUSB0'
CURRENT_OFFSET = 0.003 # mA
WATT_OFFSET = 3 # W

HOST = 'lab11power.ddns.net'
PORT = 4908
myDevice = APS3B12.APS3B12(DEV, 1)

def main():
    if sys.version_info[0] < 3:
        raise 'Python 3 required to run this script'

    print('APS3B12 control script server')
    
    skt = socket.socket()
    skt.bind((HOST, PORT))

    while True:
        skt.listen(1)
        c, addr = skt.accept()
        print('connection from: {0}'.format(addr))
        while True:
            data = c.recv(1024).strip().decode('utf-8')
            if not data:
                break
            print("Command Received: {0}".format(data))
            res = cmdExec(data)
            if data == 'exit':
                break
            if res:
                c.send(bytes(str(res), 'utf-8'))
        c.close()
        print('Connection closed')
        #myDevice.load_enable(False)

def isFloat(val):
    try:
        float(val)
        return True
    except:
        return False


# supported commands:
# "on":      Turn load on
# "off":     Turn load off
# "readV":   Read voltage value
# "readI":   Read current value
# "readW":   Read wattage value
# "exit":    Exit
# "watt=XX": Set load to XX W
# "amp=XX":  Set load to XX A
def cmdExec(myStr):
    myCmd = myStr

    op1Dict = {'on':(myDevice.load_enable, True), \
              'off':(myDevice.load_enable, False), \
            'readV':(myDevice.get_value, 'V'), \
            'readI':(myDevice.get_value, 'I'), \
            'readW':(myDevice.get_value, 'W'), \
            'readBank':(myDevice.set_get_bank_wave, 'GET'), \
            'readWave':(myDevice.set_get_bank_wave, 'GET'), \
             'exit':(myDevice.load_enable, False)
              }

    if myCmd in op1Dict:
        if myCmd == 'readBank' or myCmd == 'readWave':
            tmp = 'BANK' if myCmd == 'readBank' else 'WAVE'
            res = myDevice.set_get_bank_wave('GET', tmp, 0)
            return str(res) + '\r\n'
        else:
            (myFuc, myArg) = op1Dict.get(myCmd)
            res = myFuc(myArg)
            if res:
                return res
        return 'Execute succeed\r\n'
    elif '=' in myCmd and len(myCmd.split('='))==2:
        myCmd = myCmd.split('=')
        if (myCmd[0] == 'watt' or myCmd[0] == 'amp') and isFloat(myCmd[1]):
            # set watt or amp
            tmpType = 'W' if myCmd[0] == 'watt' else 'I'
            tmpOffset = WATT_OFFSET if myCmd[0] == 'watt' else CURRENT_OFFSET
            value = float(myCmd[1])
            tryValue = value
            # recursively correct the setting
            while True:
                tmp = myDevice.set_value(tmpType, tryValue)
                if tmp < 0:
                    break
                offset = tmp - value
                if abs(offset) <= tmpOffset:
                    break
                tryValue -= offset
            if tmp > 0:
                print('Settle to {:} {:}'.format(tmp, tmpType))
                return tmp
        elif (myCmd[0] == 'bank' or myCmd[0] == 'wave') and isFloat(myCmd[1]):
            myDevice.set_get_bank_wave('SET', myCmd[0].upper(), int(myCmd[1]))
            tmp = myDevice.set_get_bank_wave('GET', myCmd[0].upper(), 0)
            print('Set ' + myCmd[0].upper() + ' to ' + str(tmp))
            return str(tmp) + '\r\n'
    return 'Invalid Command\r\n'
    

if __name__=="__main__":
    main()
