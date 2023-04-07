'''
This is rpi-chassis.py. It is the primary program that runs the RPi Chassis.
The live navigation and object detection will reside within this program.
'''

# Our required libaries
import time 				# Used to sleep
from picarx import Picarx 		# Import our Picarx object
from picamera import PiCamera		# Import our Picamera object
from picamera.array import PiRGBArray  	# Import the RGB array for picamera
import cv2				# Import opencv, used for object detection/image proccessing
import rpi_imu				# Import our IMU script
from rpi_gps import GPS			# Import our GPS script
# Import tflite, used for running an object-detection model
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

#Making these easy to change so that its easier to test
NUM_OBJECTS = 3 # number of objects the camera will detect
AVOID_OBJECTS = ["person", "car", "Ultrasonic"] # add things that robot should detect / avoid


# This is a helper function for object_detection. It reads in RPi Chassis object and a tuple.
# It will then update the tuple based on the ultrasonic sensors output
def ultrasonic_detect(rpi_chassis, objects):
	#print("In ultrasonic detection")

	# Check if the ultrasonic sensor detects an object
	distance = rpi_chassis.ultrasonic.read()
	print("Ultrasonic distance: " + str(distance))

	# If the distance is less than 30, we have detected an object!
	if distance < 30:
		# Set our tuple that an object has been detected
		objects.append((True,"Ultrasonic", "Center","Bottom", "300", "300"))

	return objects


#This is a helper function to determine where an object is located 
def get_obj_location(boxLocation):
	local = ''
	#Getting the coordinates of the center of the box surrounding the object (automatically generated)
	x_origin = boxLocation.origin_x
	y_origin = boxLocation.origin_y
	x_len = boxLocation.width
	x_len = x_len / 2
	y_len = boxLocation.height
	y_len = y_len /2
	x = x_origin + x_len
	y = y_origin + y_len
	x_loc = ''
	y_loc = ''
	#Determining the location using the center of the object
	if x < 128:
		x_loc = "Far Left"
	if x < 256:
		x_loc = "Left"
	elif x < 384:
		x_loc = "Center"
	elif x < 512:
		x_loc = "Right"
	else:
		x_loc = "Far Right"

	if y < 213:
		y_loc = "Top"
	elif y < 426:
		y_loc = "Middle"
	else:
		y_loc = "Bottom"

	return x_loc, y_loc


# This is a helper function for object detection. It reads in the streamed image and a tuple.
# It will update the tuple based on the camera's input.
def camera_detect(img, objects, detector):
	# Reduce the image size for reduced calculation & efficiency
	# Camera goes here
	rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	input = vision.TensorImage.create_from_array(rgb_image)
	dobject = detector.detect(input)
	#print("dobject: " + str(dobject))
	#object_detected = dobject.detections
	if dobject.detections:
		for obj in dobject.detections:
			object_detected = dobject.detections[0]
			obj_cat = obj.categories[0]
			obj_loc = obj.bounding_box
			#print("object_detected: " + str(object_detected))
			#print("obj_cat: " + str(obj_cat))
			#print("obj_loc: " + str(obj_loc))
			#Getting the object category
			obj_type = str(obj_cat.category_name)
			#print("obj_type: " + str(obj_type))
			x, y = get_obj_location(obj_loc)
			#print("locat: " + str(locat))
			objects.append((True, obj_type, str(x), str(y), obj.bounding_box.width, obj.bounding_box.height))		
	return objects



def object_detection(rpi_chassis, img, detector):
	#print("In object-detection")

	# This is what our function will return
	# List of (True/False if object detected, Type of object, X Location of object, Y Location of object, 
	# Width in pixels of object, Height in pixels of object)
	objects = []


	# Update the object based on the ultrasonic sensor input
	objects = ultrasonic_detect(rpi_chassis, objects)

	# Check if the camera has detected an object
	objects = camera_detect(img, objects, detector)

	if len(objects) == 0:
		objects.append((False, "Unknown", 0, 0, 0, 0))
	# Return the objects information
	return objects


# Note: The following 3 functions will likely be adjusted to include better accuracy/calibration
# Returns the (x,y,z) coordinates of the accelerometer
def get_accelerometer():
	return (IMU.readACCx(), IMU.readACCy(), IMU.readACCz())


# Returns the (x,y,z) coordinates of the gyrometer
def get_gyrometer():
	return (IMU.readGYRx(), IMU.readGYRy(), IMU.readGYRz())


# Returns the (x,y,z) coordinates of the magnetometer
def get_magnetometer():
	return (IMU.readMAGx(), IMU.readMAGy(), IMU.readMAGz())


# This is where the primary repeated navigation code will reside, for now it is a place holder
def navigation(objects, cur_coord, goal_coord):
	return "forward" or "left" or "right" or "backward" or "left_backward" or "right_backward"


# This function moves the rpi_chassis given a direction, for example forward, left, right, backward, etc
def move(rpi_chassis, direction):
	# If the direction is stop
	if direction == 'stop':
		# Stop the chassis
		rpi_chassis.stop()
	elif direction == 'forward':
		# Move the chassis forward
		rpi_chassis.steer_straight()
		rpi_chassis.forward(5)
	elif direction == 'left':
		# Move the chassis left
		rpi_chassis.set_dir_servo_angle(-15)
	elif direction == 'right':
		# Move the chassis right
		rpi_chassis.set_dir_servo_angle(15)
	else:
		# If any unknown direction is given ignore it
		return

# This is the main driver function
if __name__ == "__main__":
	# This try helps smoothly stop the program (making sure to stop the car)
	# Anytime there is an exception/CTRL+C
	try:
		print("Starting RPi-Chassis")
		start_time = time.time()
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
		print("Finished initializing")
		print("Elasped time: " + str(time.time()-start_time))
		# Our infinate loop for continuous object-detection and navigation
		# Get continuous input from our camera, it is an infinate loop!
		boption = core.BaseOptions(file_name='tf_lite_models/efficientdet_lite0.tflite', use_coral=True, num_threads=2)
		doption = processor.DetectionOptions(max_results=NUM_OBJECTS, score_threshold=0.6)
		options = vision.ObjectDetectorOptions(base_options=boption, detection_options=doption)
		detector = vision.ObjectDetector.create_from_options(options)
		for frame in rpi_camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
			print("\n\nBeginning of loop:")
			print("Elasped time: " + str(time.time()-start_time))
			# Convert our image into an array
			img = frame.array
			# Our list of objects, each object is (True/False, Type, X_location, Y_location, size)
			objects = object_detection(rpi_chassis, img, detector)

			cur_move = 'forward' # our default movement
			# For every object given, decide how to move
			for object in objects:
				is_object, type, x_loc, y_loc, width, height = object
				#If nothing is detected or the object is not a Person move forward
				if not is_object:
					break
				elif type == 'Ultrasonic':
					cur_move = 'stop'
				elif type not in AVOID_OBJECTS or (width < 100 and height < 200):
					print("Non-Threatening Object: " + str(type))
					break
				else:
					print("There is an object!")
					print("Object Type: " + str(type))
					print("Object Location: " + str(x_loc) + " " + str(y_loc))
					print("Object Size: " + str(width) + "W " + str(height) + "H")

					# If object is on the right, move left
					if x_loc == "Right":
						# If we have previously detected an object on the left, stop
						if cur_move == 'stop' or cur_move == 'right':
							cur_move = 'stop'
							#print("Detected object on right and left, stopping.")
						# Otherwise we just move to the left
						else:
							cur_move = 'left'
							#print("Move left")
					elif x_loc == "Left":
						# If we have previously detected an object on the right, stop
						if cur_move == 'stop' or cur_move == 'left':
							cur_move = 'stop'
							#print("Detected object on the left and right, stopping.")
						# Otherwise we jsut move to the right
						else:
							cur_move = 'right'
							#print("Move right")
					elif x_loc == "Center":
						#print("Stopping")
						cur_move = 'stop'
						break
					else:
						#print("Object not a threat, move forward")
						cur_move = 'forward'

			# Start moving
			#move(rpi_chassis, cur_move)
			'''
			print("Elasped time: " + str(time.time()-start_time))
			# Get the coordinates from the gps
			latitude, longitude = GPS.get_coordinates()
			# Print the latitude and longitude
			print("Latitude: ", latitude)
			print("Longitude: ", longitude)
	
			print("Elasped time: " + str(time.time()-start_time))
			# Get the course and speed
			course, speed = GPS.get_course_speed()
			# Print the course and speed
			print("Course: ", course)
			print("Speed: ", speed)
	
			print("Elasped time: " + str(time.time()-start_time))
			cur_coord = (latitude, longitude)
			goal_coord = (0,0)
	
			'''
			print("Elasped time: " + str(time.time() - start_time))

			# Slow down output
			#time.sleep(1)
			# Show the image
			#cv2.imshow('RPi Camera', img)
			# Release image cache
			raw_capture.truncate(0)

			#k = cv2.waitKey(1) & 0xFF
			#if k == 27:
			#	break

	except KeyBoardInterrupt:
		rpi_chassis = Picarx()
		rpi_chassis.stop()
		print("Exiting...")
	except Exception as e:
		rpi_chassis = Picarx()
		rpi_chassis.stop()
		print(e)
