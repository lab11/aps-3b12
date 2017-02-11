#! /usr/bin/python3
import APS3B12
import sys
from time import sleep

DEV = '/dev/ttyUSB0'
CURRENT_OFFSET = 0.003 # mA
WATT_OFFSET = 3 # W
MAX_TRIALS = 5 # try 5 times max

def help(inc_val):
    print("Commands:")
    print("on\tTurn load on")
    print("off\tTurn load off")
    print("readV\tRead voltage value")
    print("readI\tRead current value")
    print("readW\tRead wattage value")
    print("[watt=]XX\tSet load to XX W")
    print("amp=XX\tSet load to XX A")
    print("inc=XX\tSet increment to XX W")
    print("<enter>\tIncrement wattage by {:} W".format(inc_val))
    print("help\tDisplay help")
    print("exit\tTurn load off and exit application\n")

def main():

	reset = True if len(sys.argv) != 2 else False

    input_watt = 0
    inc_watt = 25
    if(reset):
        print("\nAPS 3B12 Control Script\n")
        help(inc_watt)

    myDevice = APS3B12.APS3B12(DEV, reset)

    #if(len(sys.argv) == 2):
    if(!reset):
        if(sys.argv[1] == 'read'):
            voltage = '{:.3f}'.format(myDevice.get_value('V'))
            power = '{:.3f}'.format(myDevice.get_value('W'))
            print('[' + voltage + ',' + power + ']')
            exit()
        elif(sys.argv[1].isdigit()):
            myDevice.set_value('W', sys.argv[1])
            voltage = '{:.3f}'.format(myDevice.get_value('V'))
            power = '{:.3f}'.format(myDevice.get_value('W'))
            print('[' + voltage + ',' + power + ']')
            exit()
    else:
        op1Dict = {'on':(myDevice.load_enable, True), \
                  'off':(myDevice.load_enable, False), \
                'readV':(myDevice.get_value, 'V'), \
                'readI':(myDevice.get_value, 'I'), \
                'readW':(myDevice.get_value, 'W'), \
                 'help':(help, inc_watt),\
                 'exit':(myDevice.load_enable, False)
                  }
        while(1):
            textIn = input('Enter input: ')
            textIn = textIn.split('=')
            command = textIn[0].strip(' ')
            # no command, simply increment by inc_watt
            if len(textIn[0]) == 0:
                input_watt += inc_watt
                myDevice.set_value('W', input_watt)
            # No-parameter commands
            elif len(textIn) == 1:
                if command == 'on':
                    print("Load turning on...")
                    myDevice.load_enable(True)
                elif command == 'off':
                    print("Load turning off...")
                    myDevice.load_enable(False)
                elif command == 'readV':
                    voltage = myDevice.get_value('V')
                    print('Voltage : {:.3f} (V)'.format(voltage))
                elif command == 'readI':
                    current = myDevice.get_value('I')
                    print('Current: {:.3f} (A)'.format(current))
                elif command == 'readW':
                    power = myDevice.get_value('W')
                    print('Current: {:.3f} (W)'.format(power))
                elif command.isdigit():
                    input_watt = command
                    myDevice.set_value('W', input_watt)
                elif command == 'help':
                    help(inc_watt)
                elif command == 'exit':
                    print("Exiting...")
                    myDevice.load_enable(False)
                    break
                else:
                    print('Unrecognized command')
            elif len(textIn) == 2:
                value = float(textIn[1].strip(' '))
                if command == 'watt' or command == 'amp':
                    if command == 'watt':
                        input_watt = value
                    tmpType = 'W' if command == 'watt' else 'I'
                    tmpOffset = WATT_OFFSET if command == 'watt' else CURRENT_OFFSET
                    tryValue = value
                    trials = 0
                    # recursively correct the setting
                    while trials < MAX_TRIALS:
                        tmp = myDevice.set_value(tmpType, tryValue)
                        if tmp < 0:
                            break
                        offset = tmp - value
                        if abs(offset) <= tmpOffset:
                            break
                        tryValue -= offset
                        trials += 1
                    if tmp > 0:
                        print('Settle to {:} {:}'.format(tmp, tmpType))
                elif command == 'inc':
                    inc_watt = value
                    print("Increment value set to {:} W".format(inc_watt))
            else:
                print('Unrecognized command')


if __name__=='__main__':
    main()

