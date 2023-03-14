# Used for input processing/delay
import time
import readchar
# Import our Picarx object
from picarx import Picarx
# Import our Picamera object
from picamera import PiCamera
from picamera.array import PiRGBArray
# Import Open CV
import cv2

def print_welcome():
	print("Welcome to Test Sensors")
	print("-----------------------")
	print("U: Ultrasonic Sensor")
	print("L: Grayscale Sensor")
	print("C: Camera")
	print("G: GPS") 
	print("Q: Quit")
def test_ultrasonic(rpichassis):
	print_welcome()
	print("Ultrasonic Distance: " + str(rpichassis.ultrasonic.read()))
def test_grayscale(rpichassis):
	print_welcome()
	print("Grayscale Value: " + str(rpichassis.get_grayscale_data()))
def test_camera():
	print_welcome()
	# Initialize our PiCamera object
	with PiCamera() as cam:
		cam.resolution = (640,480) # Our Camera can support other but at slower FPS
		cam.framerate = 90
		rawCapture = PiRGBArray(cam, size=cam.resolution)
		time.sleep(2)

		for frame in cam.capture_continuous(rawCapture, format='bgr', use_video_port=True):
			img = frame.array
			cv2.imshow("RPi Chassis Camera", img)
			rawCapture.truncate(0)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

		print("Exiting Camera")
		cv2.destroyAllWindows()
		cam.close()
def test_gps():
	print_welcome()
	print("Sorry GPS testing unavailable at this time")



if __name__ == "__main__":
	# Initialize our Picarx object
	rpichassis = Picarx()
	# Print the welcome message to the user
	print_welcome()

	# Out inifinite while loop (until user exits)
	while True:
		# Read in the next character from the terminal
		key = readchar.readkey()
		# Lowercase the read in character
		key = key.lower()

		# If the key is one of the listed commands
		if key in('ulcgq'):
		# If u, print the output of the ultrasonic sensor
			if 'u' == key:
				test_ultrasonic(rpichassis)
			# If l, print the output of the grayscale sensor
			elif 'l' == key:
				test_grayscale(rpichassis)
			# If c, record and display from the camera
			elif 'c' == key:
				test_camera()
			# If g, print the output of the GPS
			elif 'g' == key:
				test_gps()
			# If q, print quit and end the loop
			elif 'q' == key:
				print("\nQuit")
				break
			# Add a small input delay between changing commands
			time.sleep(.05)
		# Add a small char input delay
		time.sleep(.02)
