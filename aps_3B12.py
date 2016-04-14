#! /usr/bin/python3
import APS3B12
from time import sleep

DEV = '/dev/ttyUSB0'
OFFSET_THRESHOLD = 0.003 # mA

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
	print("\nAPS 3B12 Control Script\n")
	input_watt = 0
	inc_watt = 25
	help(inc_watt)
	myDevice = APS3B12.APS3B12(DEV)

	while(1):
		textIn = input('Enter input: ')
		textIn = textIn.split('=')
		command = textIn[0].strip(' ')
		# no command, simply increment by inc_watt
		if len(textIn[0]) == 0:
			input_watt += inc_watt
			#print('increment the load to {:} (W)'.format(input_watt))
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
			if command == 'watt':
				input_watt = value
				myDevice.set_value('W', input_watt)
			elif command == 'amp':
				tryValue = value
				while True:
					myDevice.set_value('I', tryValue)
					sleep(1)
					tmp = myDevice.get_value('I')
					offset = tmp - value
					if abs(offset) <= OFFSET_THRESHOLD:
						break
					tryValue -= offset
				print('Settle to {:} (A)'.format(tmp))
			elif command == 'inc':
				inc_watt = value
				print("Increment value set to {:} W".format(inc_watt))
		else:
			print('Unrecognized command')


if __name__=='__main__':
	main()

