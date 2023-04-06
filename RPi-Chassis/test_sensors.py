'''
Welcome to test_sensors.py! 			Author: Bridgette Bryant
This program was created to test all the sensors on the RPi-Chassis.
It has several functons:

main:
	This is the main driver program. It utilizes the other functions.
	Primarily it initilizes everything, and then goes into a (forever)
	while loop. Within the loop it reads in the next character from the
	terminal. If the character read is one of the valid characters to
	test one of the sensors it will call the appropriate function.

print_welcome:
	This simply prints a welcome message and the correlating keys to 
	test each sensors on the RPi-Chassis.

test_ultrasonic:
	Prints the output of ultrasonic sensor to the user.

test_grayscale:
	Prints the output of the grayscale sensor to the user.

test_camera:
	Displays the output of the camera to the user.

test_gps:
	Currently not implemented, the plan is to have it print the Longitude,
	Lagitude, and Course output of GPS to the user.

test_accelerometer:
	Displays the x,y,z output of the accelerometer to the user.

test_gyrometer:
	Displays the x,y,z output of the gyrometer to the user.

test_magnetometer:
	Displays the x,y,z output of the  magnetometer to the user.

'''

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
# Import our IMU script
from rpi_imu import IMU
# Import our GPS script
from rpi_gps import GPS

# Prints the welcome message to the user with keypress directions
def print_welcome():
	print("Welcome to Test Sensors")
	print("-----------------------")
	print("U: Ultrasonic Sensor")
	print("L: Grayscale Sensor")
	print("C: Camera")
	print("G: GPS")
	print("A: Accelerometer")
	print("Y: Gyrometer")
	print("M: Magnetometer")
	print("Q: Quit")


# Prints the output reading of the ultrasonic sensor
def test_ultrasonic(rpichassis):
	print_welcome()
	print("Ultrasonic Distance: " + str(rpichassis.ultrasonic.read()))


# Prints the output reading of the grayscale sensor
def test_grayscale(rpichassis):
	print_welcome()
	print("Grayscale Value: " + str(rpichassis.get_grayscale_data()))


# Displays the output of the camera, requires 'ESC' to exit
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


# Prints GPS output, not currently implemented
def test_gps():
	print_welcome()
	latitude, longitude = GPS.get_coorindates()
	print("Latitude: " + str(latitude))
	print("Longitude: " + str(longitude))
	course, speed = GPS.get_course_speed()
	print("Course: " + str(course))
	print("Speed: " + str(speed))


# Prints the x,y,z coordinates of the accelerometer
def test_accelerometer():
	print_welcome()
	print("Accelerometer:")
	print("x: " + str(IMU.readACCx()))
	print("y: " + str(IMU.readACCy()))
	print("z: " + str(IMU.readACCz()))


# Prints the x,y,z coordinates of the gyrometer
def test_gyrometer():
	print_welcome()
	print("Gyrometer")
	print("x: " + str(IMU.readGYRx()))
	print("y: " + str(IMU.readGYRy()))
	print("z: " + str(IMU.readGYRz()))


# Prints the x,y,z coordinates of the magnetometer
def test_magnetometer():
	print_welcome()
	print("Magnetometer")
	print("x: " + str(IMU.readMAGx()))
	print("y: " + str(IMU.readMAGy()))
	print("z: " + str(IMU.readMAGz()))



# This is the main driver function
if __name__ == "__main__":

	# Initialize our Picarx object
	rpichassis = Picarx()

	# Detect and Initialize our IMU
	IMU.detectIMU()
	if IMU.BerryIMUversion == 99:
		print("No Berry IMU Found!")
	else:
		IMU.initIMU()

	# Print the welcome message to the user
	print_welcome()

	# Out infinite while loop (until user exits)
	while True:
		# Read in the next character from the terminal
		key = readchar.readkey()
		# Lowercase the read in character
		key = key.lower()

		# If the key is one of the listed commands
		if key in('ulcgaymq'):
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
			# If a, print the output of the accelerometer
			elif 'a' == key:
				test_accelerometer()
            		# If y, print the output of the gyrometer
			elif 'y' == key:
				test_gyrometer()
			# If m, print the output of the magnetometer
			elif 'm' == key:
				test_magnetometer()
			# If q, print quit and end the loop
			elif 'q' == key:
				print("\nQuit")
				break

			# Add a small input delay between changing commands
			time.sleep(.05)

		# Add a small char input delay
		time.sleep(.02)
