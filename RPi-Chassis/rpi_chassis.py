'''
This is rpi-chassis.py. It is the primary program that runs the RPi Chassis.
The live navigation and object detection will reside within this program.
'''

# Our required libaries
import time 				# Used to sleep
from picarx import Picarx 		# Import our Picarx object
from picamera import PiCamera		# Import our Picamera object
from picarmera.array import PiRGBArray  # Import the RGB array for picamera
import cv2				# Import opencv, used for object detection/image proccessing



def object_detection(rpi_chassis, rpi_camera):
	print("In object-detection")

	# This is what our function will return
	# (True/False if object detected, Type of object, Location of Object)
	object = (False, "unknown", "unknown")

	# Check if the ultrasonic sensor detects an object
	distance = rpi_chassis.ultrasonic.read()
	print("Ultrasonic distance: " + str(distance))
	
	# If the distance is less than 30, we have detected an object!
	if distance < 30:
		# Set our tuple that an object has been detected
		object = (True, "unknown", "center")

	# Check if the camera has detected an object

# This is the main driver function
if __name__ == "__main__":
	# Initialize the PicarX object for our RPi Chassis
	rpi_chassis = Picarx()
	# Initilize the 
