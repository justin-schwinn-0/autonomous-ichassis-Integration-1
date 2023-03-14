# Used for input processing
#import pygame
#from pygame.locals import *
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
    print("A: Left")
    print("S: Backward")
    print("D: Right")
    print("E: Stop")
    print("ESC: To quit")

# This is the main driver function
if __name__ == "__main__":
    # Initialize our Picarx object
    rpichassis = Picarx()
    # Initialize our pygame:
    #pygame.init()
    #screen = pygame.display.set_mode((240, 240))
    #pygame.display.set_caption('RPi Chassis')
    # Print the welcome message to the user
    print_welcome()
    
    # Our inifinite while loop (until user exits)
    while True:
        # Sleep to slightly delay input
        #time.sleep(.02)

        key = readchar.readkey()
        key = key.lower()

        if key in('wasde'):
            if 'w' == key:
                rpichassis.forward(50)
            elif 's' == key:
                rpichassis.backward(50)
            elif 'a' == key:
                rpichassis.leftTurn()
            elif 'd' == key:
                rpichassis.rightTurn()
            elif 'e' == key:
                rpichassis.stop()

            time.sleep(.05)

        elif key == readchar.key.CTRL_C or key in readchar.key.ESCAPE_SEQUENCES:
            rpichassis.stop()
            print("\n Quit")
            break

        time.sleep(.02)

        '''   
        # Get the user input using pygame
        for event in pygame.event.get():
            # If the event is a pressed key
            if event.type == pygame.KEYDOWN:
                # user_input = raw_input()
            
                # Process the input
                #user_input = user_input.lower()
                #user_input = user_input.strip()
        
                # Move based on the input
                if event.key == 'c':
                    # Stop the chassis and break the loop
                    rpichassis.stop()
                    print("Exiting...")
                    break
                elif event.key == K_w:
                    # Move the chassis forward
                    rpichassis.forward(50)
                elif event.key == K_a:
                    # Move the chassis left
                    rpichassis.leftTurn()
                elif event.key == K_s:
                    # Move the chassis backward
                    rpichassis.backward(50)
                elif event.key == K_d:
                    # Move chassis right
                    repichassis.rightTurn()
                
        '''