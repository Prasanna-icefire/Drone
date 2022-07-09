from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import firebase_admin
from firebase_admin import db
import argparse
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebaseAuth.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
docs = db.collection('sos').get()
for doc in docs:
    lat = doc.to_dict()["location"].latitude
    lon = doc.to_dict()["location"].longitude

#print(lat,lon)
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect

print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(10)
print("Setting default/target airspeed to 3")
vehicle.airspeed = 3

point1 = LocationGlobalRelative(lat, lon, 20)
vehicle.simple_goto(point1)
time.sleep(30)
#vehicle.mode = VehicleMode("RTL")

vehicle.close()
