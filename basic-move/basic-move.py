from picarx import Picarx
import time



# These are the basic movement commands for the robot. We created a new class based of off the initial class
# in sunflower's picarx.py files so that we could make the navigation slightly easier. We wanted the robot
# to automatically turn 90 degrees as a parking lot is essentially a grid. By creating a single class for all
# movement we make it far easier to use later.

robo = Picarx

class Robot:

    # The given function for moving forward was already speed based so we just used the same one.
    def forward(speed):
        robo.forward(speed)

    # The given function for moving forward was already speed based so we just used the same one.
    def back(speed):
        robo.backward(speed)

    def stop():
        robo.stop()

    # This is the code for the left turn. Currently needs testing. I'm hoping we'll get a sharper turn
    # by only using the outer motor (in this case the right motor) and adjusting the direction servos angle
    # but it will need further testing to ensure perfection.
    def leftTurn():
        robo.set_dir_servo_angle(30)
        robo.set_motor_speed(1, 30)
        time.sleep(.25)
        robo.stop()
        robo.set_dir_servo_angle(0)
    
    # This is the function to turn right. It uses the same logic as the previous function and will need some
    # testing to ensure functionality.
    def rightTurn():
        robo.set_dir_servo_angle(-30)
        robo.set_motor_speed(2, 30)
        time.sleep(.25)
        robo.stop()
        robo.set_dir_servo_angle(0)

