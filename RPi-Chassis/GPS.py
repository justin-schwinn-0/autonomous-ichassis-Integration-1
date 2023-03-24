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


# Parses the $GPGLL string and returns a tuple of its important outputs
# (Latitude, N/S, Longitude, E/W, UTC Time, Status)
def parse_gpgll(gpgll):
    gpgll_list = gpgll.split(',')
    #print(len(gpgll_list))
    #print(gpgll_list)

    # Skip the first field Message ID($GPGLL)
    # The second field is Latitude (ddmm.mmmm), third is N/S indicator
    #print("\nraw latitude: " + str(gpgll_list[1]) + " " + str(gpgll_list[2]))
    # The fourth field is Longitude (dddmm.mmmm), fifth is E/W indicator
    #print("raw longitude: " + str(gpgll_list[3]) + " " + str(gpgll_list[4]))
    # The sixth is the UTC time
    #print("utc time: " + str(gpgll_list[5]))
    # The seventh is the status (A is valid data, V is invalid data)
    #print("status: " + str(gpgll_list[6]))
    # Return the important values
    return (gpgll_list[1], gpgll_list[2], gpgll_list[3], gpgll_list[4], gpgll_list[5], gpgll_list[6])


# Parses the $GPVTG string and returns a tuple of its important outputs
# (Course, Reference, Speed, Units)
def parse_gpvtg(gpvtg):
    gpvtg_list = gpvtg.split(',')
    #print(len(gpvtg_list))
    #print(gpvtg_list)

    # Skip the first field Message ID($GPVTG)
    # The second field is the Course in degrees and their reference (True)
    #print("course: " + str(gpvtg_list[1]) + " " + gpvtg_list[2])
    # The eighth is the speed in kilometers
    #print("status: " + str(gpvtg_list[7]) + " " + str(gpvtg_list[8]))
    # Return the important values
    return (gpvtg_list[1], gpvtg_list[2], gpvtg_list[7], gpvtg_list[8])


# Converts the raw latitude input into decimal degrees (google maps friendly)
def convert_latitude(raw_lat, dir):
    # Our original format is ddmm.mmmm (d = decimal degrees, m = decimal minutes)
    # For google maps we need it to be in dd.dddd format (north is positive, south is negative
    # First we will parse our raw latitude input
    dd = raw_lat[:2]
    mm_mmmm = raw_lat[2:]
    #print("dd: " + dd + " mm.mmmm: " + mm_mmmm)

    # Next we will convert 'mm.mmmm' to '.dddd' by dividing by 60
    dddd = float(mm_mmmm) / 60
    dddd = float("{:.4f}".format(dddd))
    #print("dddd: " + str(dddd))

    # Add the dd and .dddd together
    dd_dddd = float(dd) + dddd
    #print("dd_dddd: " + str(dd_dddd))

    # Finally we will make it negative if it is pointing south
    if dir == 'S':
        dd_dddd *= -1
        #print("dd_dddd: " + str(dd_dddd))

    # Return the converted latitude
    return dd_dddd


# Converts the raw longitude input into decimal degrees (google maps friendly)
def convert_longitude(raw_lon, dir):
    # Our original format is dddmm.mmmm (d = decimal degrees, m = decimal minutes)
    # For google maps we need it to be in dd.dddd format (east is positive, west is negative
    # First we will parse our raw latitude input
    ddd = raw_lon[:3]
    mm_mmmm = raw_lon[3:]
    #print("ddd: " + ddd + " mm.mmmm: " + mm_mmmm)

    # Next we will convert 'mm.mmmm' to 'dd.dddd' by dividing by 60
    dd_dddd = float(mm_mmmm) / 60
    dd_dddd = float("{:.4f}".format(dd_dddd))
    #print("dd_dddd: " + str(dd_dddd))

    # Add the ddd and dd.dddd together
    ddd_dddd = float(ddd) + dd_dddd
    #print("dd_dddd: " + str(ddd_dddd))

    # Finally we will make it negative if it is pointing west
    if dir == 'W':
        ddd_dddd *= -1
        #print("ddd_dddd: " + str(ddd_dddd))

    # Return the converted longitude
    return ddd_dddd


# Returns the google-maps friendly coordinates (latitude, longitude)
def get_coorindates():
    # Get input from read_gps until we recieve input in $GPGLL
    gps_input = read_gps()
    while gps_input[:6] != '$GPGLL':
        gps_input = read_gps()

    # After getting the GPGLL input parse it
    gpgll = parse_gpgll(gps_input)
    # Next we can get the calculated latitude
    latitude = convert_latitude(gpgll[0], gpgll[1])
    # Next we can get the calculated longitude
    longitude = convert_longitude(gpgll[2], gpgll[3])

    # Finally we can return the calculated latitude and longitude
    return (latitude, longitude)


# Returns the course angle from the 'True' reference and the speed in Kilometers/Hr
def get_course_speed():
    # Get input from the read_gps until we recieve input in $GPVTG
    gps_input = read_gps()
    while gps_input != '$GPVTG':
        gps_input = read_gps()

    # After getting the GPVTG input parse it
    gpvtg = parse_gpvtg(gps_input)
    # Next return the course value and the speed
    return (gpvtg[0], gpvtg[2])

connect_bus()

#while True:
#   read_gps()
#   time.sleep(gps_read_interval)
