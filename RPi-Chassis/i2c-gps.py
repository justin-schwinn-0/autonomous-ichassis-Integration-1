import time
import signal
import sys
import pigpio

address = 0x42
gpsReadInterval = 0.03
SDA=2
SCL=3
pi = pigpio.pi()
pi.set_pull_up_down(SDA, pigpio.PUD_UP)
pi.set_pull_up_down(SCL, pigpio.PUD_UP)
pi.bb_i2c_open(SDA,SCL,100000)
'''
def handle_ctrl_c(signal, frame):
	pi.bb_i2c_close(SDA)
	pi.stop()
	sys.exit(130)

# This will capture exit when using CTRL-C
signal.signal(signal.SIGINT, handle_ctrl_c)

def readGPS():
	c = None
	response = []
	
	while True:
		# Bit bang I2C read. 2 = Start, 6 = Read, 1 = How many bytes to read
		a = pi.bb_i2c_zip(SDA, [4, address, 2, 6, 1])
		c = ord(a[1])

		if c == 255:
			return False
			
		elif c == 10:
			break
		else:
			response.append(c)
	# Convert list to string
	gpsChars = ' '.join(chr(c) for c in response)
	print(gpsChars)

	while True:
		readGPS()
		time.sleep(gpsReadInterval)

'''
