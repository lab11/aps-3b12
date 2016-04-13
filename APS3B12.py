
import serial
import time
import sys



class APS3B12(object):

	def serial_write_byte_UTF8(self, text):
		self.serial.write(text.encode(encoding="utf-8"))
		time.sleep(.03)

	def load_enable(self, enable):
		# remote only mode
		self.serial_write_byte_UTF8('REM;')
		if enable:
			print('Enabling load')
			self.serial_write_byte_UTF8('LOAD 1;')
			self.state = True
		else:
			print('Disabling load')
			self.serial_write_byte_UTF8('CC:A 0;')
			self.serial_write_byte_UTF8('LOAD 0;')
			self.state = False
		# local only mode
		self.serial_write_byte_UTF8('LOC;')

	def __init__(self, dev):
		try:
			self.serial = serial.Serial(dev, 9600)
		except:
			sys.exit('Cannot find {:}'.format(dev))
		self.state = False
		# remote only mode
		self.serial_write_byte_UTF8('REM;')
		# turn off load
		self.load_enable(self.state)
		# local only mode
		self.serial_write_byte_UTF8('LOC;')

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
	
	def set_value(self, valType, value):
		if not self.state:
			print("Load not enabled, command ignored")
			return
		# remote only mode
		self.serial_write_byte_UTF8('REM;')
		value = float(value)
		if valType == 'I':
			self.serial_write_byte_UTF8('CC:A ' + str(value) + ';')
			print('Setting current to {:.3f} (A)'.format(value))
		elif valType == 'W':
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
		time.sleep(0.5)
		self.get_value(valType)

