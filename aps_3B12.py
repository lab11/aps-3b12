#! /usr/bin/python3
import APS3B12
from time import sleep

DEV = '/dev/ttyUSB0'
OFFSET_THRESHOLD = 0.003 # mA

def error_msg():
	print('Unrecognized command')
	#print('Valid options are:')
	#print('on - activate load')
	#print('off - deactivate load')
	#print('exit - quit application')
	
def help():
	print("Commands:")
	print("on\tTurn load on")
	print("off\tTurn load off")
	print("readV\tRead voltage value")
	print("readI\tRead current value")
	print("readW\tRead wattage value")
	print("watt=XX\tSet load to XX W")
	print("amp=XX\tSet load to XX A")
	print("help\tDisplay help")
	print("exit\tTurn load off and exit application\n")

def main():
	print("\nAPS 3B12 Control Script\n")
	help()
	myDevice = APS3B12.APS3B12(DEV)
	#myDevice.get_loadState()
	# For each command:
	#	1. Set 3B12 to Remote
	#	2. Perform operation
	#	3. Set 3B12 to Local

	while(1):
		textIn = input('Enter input: ')
		textIn = textIn.split('=')
		command = textIn[0].strip(' ')
		# No-parameter commands
		if len(textIn) == 1:
			if(command == 'on'):
				print("Load turning on...")
				myDevice.load_enable(True)
			elif(command == 'off'):
				print("Load turning off...")
				myDevice.load_enable(False)
			elif(command == 'readV'):
				voltage = myDevice.get_value('V')
				print('Voltage : {:.3f} (V)'.format(voltage))
			elif(command == 'readI'):
				current = myDevice.get_value('I')
				print('Current: {:.3f} (A)'.format(current))
			elif(command == 'readW'):
				power = myDevice.get_value('W')
				print('Current: {:.3f} (W)'.format(power))
			elif(command == 'help'):
				help()
			elif(command == 'exit'):
				print("Exiting...")
				myDevice.load_enable(False)
				break
			else:
				error_msg()
		elif len(textIn) == 2:
			value = float(textIn[1].strip(' '))
			if command == 'watt':
				myDevice.set_value('W', value)
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
		else:
			error_msg()


if __name__=='__main__':
	main()

