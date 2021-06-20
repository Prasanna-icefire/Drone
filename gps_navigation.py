import dronekit
import time
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
import math

def get_distance_metresy(x,y, aLocation2):
    dlat = aLocation2.lat - x
    dlong = aLocation2.lon - y
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def gotoLocation(x,y):
    vehicle.airspeed = 0.5
    point = LocationGlobalRelative(x,y,vehicle.location.global_frame.alt)
    vehicle.simple_goto(point,groundspeed=0.5)
    print("Heading to Location")
    while get_distance_metresmy(x,y,vehicle.location.global_frame) > 3:
        print("Remaining Distance %s",get_distance_metresmy(x,y,vehicle.location.global_frame))
        time.sleep(0.1)
    print("Drone_Station B reached")

def get_location_metres(original_location, dNorth, dEast):
    earth_radius = 6378137.0
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;

def arm_and_takeoff(aTargetAltitude):

    print ("Basic pre-arm checks")
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        time.sleep(1)

    print ("Arming motors")
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) 
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print ("Reached target altitude")
            break
        time.sleep(1)


vehicle = connect('/dev/ttyACM0', wait_ready=True,baud=57600)
print(" Global Location: %s" % vehicle.location.global_frame)

arm_and_takeoff(10)
gotoLocation(13.0216571,77.679773)
vehicle.mode = VehicleMode("LAND")
time.sleep(10)
arm_and_takeoff(2)
vehicle.mode = VehicleMode("RTL")
time.sleep(10)

vehicle.close()








