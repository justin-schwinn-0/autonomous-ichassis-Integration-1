'''
This is rpi-chassis.py. It is the primary program that runs the RPi Chassis.
The live navigation and object detection will reside within this program.
'''
# Our required libaries
import time 				# Used to sleep
from picarx import Picarx 		# Import our Picarx object
from picamera import PiCamera		# Import our Picamera object
from picarmera.array import PiRGBArray  # I




# This is the main driver function
if __name__ == "__main__":
	# Initialize the PicarX object for our RPi Chassis
