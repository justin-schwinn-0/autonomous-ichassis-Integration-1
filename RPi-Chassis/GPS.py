#! /usr/bin/python
import time
import smbus
import signal
import sys
BUS = None
address = 0x42
gps_read_interval = 0.03

# Create our GPS class
class GPS(object):

    def __init__(self):
        latitude = -1 # Our default latitude
        longitude = -1 # Our default longitude
        course = -400 # Our default course angle

def connect_bus():
    global BUS
    BUS = smbus.SMBus(1)

def parse_response(gps_line):
  if(gps_line.count(36) == 1):                           # Check #1, make sure '$' doesnt appear twice
    if len(gps_line) < 84:                               # Check #2, 83 is maximum NMEA sentence length.
        char_error = 0;
        for c in gps_line:                               # Check #3, Make sure that only readiable ASCII charaters and Carriage Return are seen.
            if (c < 32 or c > 122) and  c != 13:
                char_error+=1
        if (char_error == 0):#    Only proceed if there are no errors.
            gps_chars = ''.join(chr(c) for c in gps_line)
            if (gps_chars.find('txbuf') == -1):          # Check #4, skip txbuff allocation error
                gps_str, chk_sum = gps_chars.split('*',2)  # Check #5 only split twice to avoid unpack error
                gps_components = gps_str.split(',')
                chk_val = 0
                for ch in gps_str[1:]: # Remove the $ and do a manual checksum on the rest of the NMEA sentence
                     chk_val ^= ord(ch)
                if (chk_val == int(chk_sum, 16)): # Compare the calculated checksum with the one in the NMEA sentence
                     return str(gps_chars)

def handle_ctrl_c(signal, frame):
        sys.exit(130)

#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)

def read_gps():
    c = None
    response = []
    try:
        while True: # Newline, or bad char.
            c = BUS.read_byte(address)
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
        return parse_response(response)
    except (IOError):
        connect_bus()
    except (Exception,e):
        print(str(e))


def get_latitude():
    # Get input from read_gps
    gps_input = read_gps

connect_bus()

while True:
    read_gps()
    time.sleep(gps_read_interval)
