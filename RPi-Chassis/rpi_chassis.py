'''
This is rpi-chassis.py. It is the primary program that runs the RPi Chassis.
The live navigation and object detection will reside within this program.
'''

# Our required libaries
import time 							# Used to sleep
from picarx import Picarx 				# Import our Picarx object
from picamera import PiCamera			# Import our Picamera object
from picarmera.array import PiRGBArray  # Import the RGB array for picamera
import cv2								# Import opencv, used for object detection/image proccessing
import tensorflow						# Import tensorflow, used for running an object-detection model

# This is a helper function for object_detection. It reads in RPi Chassis object and a tuple.
# It will then update the tuple based on the ultrasonic sensors output
def ultrasonic_detect(rpi_chassis, object):
	print("In ultrasonic detection")

	# Check if the ultrasonic sensor detects an object
	distance = rpi_chassis.ultrasonic.read()
	print("Ultrasonic distance: " + str(distance))

	# If the distance is less than 30, we have detected an object!
	if distance < 30:
		# Set our tuple that an object has been detected
		object = (True, "unknown", "center")

	return object


# This is a helper function for object detection. It reads in the streamed image and a tuple.
# It will update the tuple based on the camera's input.
def camera_detect(img, object):
	# Reduce the image size for reduced calculation & efficiency
	# Camera goes here




def object_detection(rpi_chassis, img):
	print("In object-detection")

	# This is what our function will return
	# (True/False if object detected, Type of object, Location of Object)
	object = (False, "unknown", "unknown")

	# Update the object based on the ultrasonic sensor input
	object = ultrasonic_detect(rpi_chassis, object)

	# Check if the camera has detected an object
	object = camera_detect(img, object)

	# Return the object information
	return object


# This is where the primary repeated navigation code will reside, for now it is a place holder
def navigation(object, long, lat):
	return 'Forward'

# This is the main driver function
if __name__ == "__main__":
	print("Starting RPi-Chassis")
	# Initialize the PicarX object for our RPi Chassis
	rpi_chassis = Picarx()
	# Initilize the Picamera object
	rpi_camera = PiCamera()
	# Set the camera's resolution and framerate
	rpi_camera.resolution = (640,480) 	# Our camera can support other but at slower FPS
	rpi_camera.framerate = 90			# Our camera can support 90 fps
	# Create our rgb array for camera
	raw_capture = PiRGBArray(rpi_camera, size=rpi_camera.resolution)
	# Allow the camera to warm up
	time.sleep(2)

	# Our infinate loop for continuous object-detection and navigation
	while True:
		# Get continuous input from our camera NOTE: This is also an infiniate loop!
		for frame in rpi_camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
			# Convert our image into an array
			img = frame.array
			# Detect objects using the object detection function
			is_object, object_type, object_location = object_detection(rpi_chassis, img)

			# If there is an object
			if is_object:
				print("There is an object!")
				print("Type: " + str(object_type))
				print("Location: " + str(object_location))
			else:
				# Otherwise there is no object
				print("No object detected!")

			# Show the image
			cv2.imshow('RPi Camera', img)
			# Release image cache
			raw_capture.truncate(0)

			k = cv2.waitKey(1) & 0xFF
			if k = 27:
				break

		# Exit the while loop
		break