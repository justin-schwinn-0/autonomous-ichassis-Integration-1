# Used for input processing/delay
import time
import readchar
# Importing our Picarx object library
from picarx import Picarx



# Prints the welcome message to the console
def print_welcome():
    # Print the welcome message to the user
    print("Welcome to Remote Control RPIChassis")
    print("------------------------------------")
    print("W: Forward")
    print("A: Steer Left")
    print("S: Backward")
    print("D: Steer Right")
    print("Q: Steer Straight")
    print("E: Stop")
    print("C: To quit")

# This is the main driver function
if __name__ == "__main__":
    # Initialize our Picarx object
    rpichassis = Picarx()
    # Print the welcome message to the user
    print_welcome()
    
    # Our inifinite while loop (until user exits)
    while True:
        # Read in the next character from the terminal
        key = readchar.readkey()
        # Lowercase the read in character
        key = key.lower()

        # If the key is one of the listed commands
        if key in('wasdeqc'):
            # If w, set the motors to move forward
            if 'w' == key:
                rpichassis.forward(50)
            # If s, set the motors to move backward
            elif 's' == key:
                rpichassis.backward(50)
            # If a, set the steering servo to steer left
            elif 'a' == key:
                rpichassis.steer_left()
            # If d, set the steering servo to steer right
            elif 'd' == key:
                rpichassis.steer_right()
            # If q, set the steering servo to steer straight
            elif 'q' == key:
                rpichassis.steer_straight()
            # If e, set the motors to stop
            elif 'e' == key:
                rpichassis.stop()
            # If c, stop the motors, steer straight, and exit the loop
            elif 'c' == key:
                rpichassis.stop()
                rpichassis.steer_straight()
                print("\n Quit")
                break
            # Add a small input delay between changing commands
            time.sleep(.05)
        # Add a small char input delay
        time.sleep(.02)
