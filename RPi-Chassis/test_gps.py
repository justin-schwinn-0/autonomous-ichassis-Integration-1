def test_gpgll():
    return "$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41"
def test_gpgll_south():
    return "$GPGLL,3723.2475,S,12158.3416,E,161229.487,A,A*41"

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

def test_gpvtg():
    return "$GPVTG,309.62,T,,M,0.13,N,0.2,K,A*23"

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


print("Parsing: ")
print(str(parse_gpgll(test_gpgll())))
print(str(parse_gpvtg(test_gpvtg())))

gpgll = parse_gpgll(test_gpgll())
print("\n\nCalculating latitude:")
convert_latitude(gpgll[0], gpgll[1])

gpgll = parse_gpgll(test_gpgll_south())
print("\n\nCalculating latitude:")
convert_latitude(gpgll[0], gpgll[1])

gpgll = parse_gpgll(test_gpgll())
print("\n\nCalculating longitude:")
print(convert_longitude(gpgll[2], gpgll[3]))

gpgll = parse_gpgll(test_gpgll_south())
print("\n\nCalculating longitude:")
print(convert_longitude(gpgll[2], gpgll[3]))




