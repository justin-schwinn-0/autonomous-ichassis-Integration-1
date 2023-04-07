#! /usr/bin/python
import time
import smbus
import signal
import sys
BUS = None
address = 0x42

def connect_bus():
    global BUS
    BUS = smbus.SMBus(1)

def parse_response(gps_line):
  #print("In parse_response")
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
  return 'N/A'

def handle_ctrl_c(signal, frame):
        sys.exit(130)

#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)

def read_gps():
    #print("In read_gps")
    c = None
    response = []
    try:
        #print("In try")
        while True: # Newline, or bad char.
            c = BUS.read_byte(address)
            if c == 255:
                #print("c == 255")
                return 'N/A'
            elif c == 10:
                #print("c == 10")
                break
            else:
                #print("appending response")
                response.append(c)
        #print("returning response")
        #print("response: " + str(response))
        return parse_response(response)
    except (IOError):
        #print("IO Error")
        connect_bus()
        return 'N/A'
    except (Exception,e):
        #print("Exception")
        print(str(e))
        return 'N/A'


# Parses the GLL string and returns a tuple of its important outputs
# (Latitude, N/S, Longitude, E/W, UTC Time, Status)
def parse_gll(gll):
    gll_list = gll.split(',')
    #print(len(gll_list))
    #print(gll_list)

    # Skip the first field Message ID($GNGLL)
    # The second field is Latitude (ddmm.mmmm), third is N/S indicator
    #print("\nraw latitude: " + str(gll_list[1]) + " " + str(gll_list[2]))
    # The fourth field is Longitude (dddmm.mmmm), fifth is E/W indicator
    #print("raw longitude: " + str(gll_list[3]) + " " + str(gll_list[4]))
    # The sixth is the UTC time
    #print("utc time: " + str(gll_list[5]))
    # The seventh is the status (A is valid data, V is invalid data)
    #print("status: " + str(gll_list[6]))
    # Return the important values
    return (gll_list[1], gll_list[2], gll_list[3], gll_list[4], gll_list[5], gll_list[6])


# Parses the VTG string and returns a tuple of its important outputs
# (Course, Reference, Speed, Units)
def parse_vtg(vtg):
    vtg_list = vtg.split(',')
    #print(len(vtg_list))
    #print(vtg_list)

    # Skip the first field Message ID($GPVTG)
    # The second field is the Course in degrees and their reference (True)
    #print("course: " + str(vtg_list[1]) + " " + vtg_list[2])
    # The eighth is the speed in kilometers
    #print("status: " + str(vtg_list[7]) + " " + str(vtg_list[8]))
    # Return the important values
    return (vtg_list[1], vtg_list[2], vtg_list[7], vtg_list[8])


# Converts the raw latitude input into decimal degrees (google maps friendly)
def convert_latitude(raw_lat, dir):
    # Verify both fields are not emtpy
    if len(raw_lat) == 0 or len(dir) == 0:
        return None
    # Our original format is ddmm.mmmm (d = decimal degrees, m = decimal minutes)
    # For google maps we need it to be in dd.dddd format (north is positive, south is negative
    # First we will parse our raw latitude input
    dd = raw_lat[:2]
    mm_mmmm = raw_lat[2:]
    #print("dd: " + dd + " mm.mmmm: " + mm_mmmm)

    # Next we will convert 'mm.mmmm' to '.dddd' by dividing by 60
    dddd = float(mm_mmmm) / 60
    #dddd = float("{:.4f}".format(dddd))
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
    # Verify both fields are not empty
    if len(raw_lon) == 0 or len(dir) == 0:
        return None
    # Our original format is dddmm.mmmm (d = decimal degrees, m = decimal minutes)
    # For google maps we need it to be in dd.dddd format (east is positive, west is negative
    # First we will parse our raw latitude input
    ddd = raw_lon[:3]
    mm_mmmm = raw_lon[3:]
    #print("ddd: " + ddd + " mm.mmmm: " + mm_mmmm)

    # Next we will convert 'mm.mmmm' to 'dd.dddd' by dividing by 60
    dd_dddd = float(mm_mmmm) / 60
    #dd_dddd = float("{:.4f}".format(dd_dddd))
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
def get_coordinates():
    # Get input from read_gps until we recieve input in GLL
    gps_input = str(read_gps())
    while str(gps_input[3:6]) != 'GLL':
        gps_input = read_gps()

    # After getting the GPGLL input parse it
    gll = parse_gll(gps_input)
    # Next we can get the calculated latitude
    latitude = convert_latitude(gll[0], gll[1])
    # Next we can get the calculated longitude
    longitude = convert_longitude(gll[2], gll[3])

    # Finally we can return the calculated latitude and longitude
    return (latitude, longitude)


# Returns the course angle from the 'True' reference and the speed in Kilometers/Hr
def get_course_speed():
    # Get input from the read_gps until we recieve input in VTG
    gps_input = str(read_gps())
    while str(gps_input[3:6]) != 'VTG':
        gps_input = read_gps()

    # After getting the VTG input parse it
    vtg = parse_vtg(gps_input)
    # Next return the course value and the speed
    return (vtg[0], vtg[2])

connect_bus()

#while True:
   #print(read_gps())
   #print(get_coordinates())
   #print(get_course_speed())

