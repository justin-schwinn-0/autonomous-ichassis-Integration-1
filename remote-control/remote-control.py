# Used for input processing
import pygame
from pygame.locals import *
import time
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
    print("C: To quit")

# This is the main driver function
if __name__ == "__main__":
    # Initialize our Picarx object
    rpichassis = Picarx()
    # Initialize our pygame:
    pygame.init()
    screen = pygame.display.set_mode((240, 240))
    pygame.display.set_caption('RPi Chassis')
    # Print the welcome message to the user
    print_welcome()
    
    # Our inifinite while loop (until user exits)
    while True:
        # Sleep to slightly delay input
        time.sleep(.02)
        
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
                
