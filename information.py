import time
import requests
import math
import json
from datetime import datetime
import time


# This library client class that connects to and accesses AWS IoT over MQTT
# AWSIotMQTTShadowClient is the client class used for device shadow operations with AWS IoT
# AWSIoTMQTTShadowClient has a method shadowUpdate() for updating the device shadow
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

# Client identifier used to connect to AWS IoT
SHADOW_CLIENT = "myShadowClient"
# The unique hostname generated for this device;
HOST_NAME = "a2y0bh556vnm2-ats.iot.us-east-1.amazonaws.com"
# path to root CA file
ROOT_CA = "AmazonRootCA1.pem"
# path to private key file
PRIVATE_KEY = "ad36b930b8-private.pem.key"
# path to certificate file
CERT_FILE = "ad36b930b8-certificate.pem.crt"
# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "ISS_Thing"

# Create, configure, and connect a shadow client.
# Create an AWS IoT MQTT Client for certificate based connection
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
# Configure the host name and port number the client tries to connect to
# 8883 for TLSv1.2
myShadowClient.configureEndpoint(HOST_NAME, 8883)
# Used to configure the rootCA, private key and  certificate files
# AWS IoT uses asymmetric cryptography
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)


# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
    print()
    print("Response from AWS:")
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)


def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = 46.76, 23.6  # Coords for Cluj
    lat2, lon2 = coord1, coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)) / 1000


# send updates to AWS IOT using shadowUpdate() method every 60 seconds
# the method showUpdate() is publishing the shadow reported state on topic $aws/things/ISS_Thing/shadow/update.
while True:
    r = requests.get(url='http://api.open-notify.org/iss-now.json')
    n = requests.get(url='http://api.open-notify.org/astros.json')
    parametri = r.json()['iss_position'];
    names = n.json()['people']
    print(names)
    vector_names = []
    Names = '';

    timestamp1 = r.json()['timestamp']
    timp_curent = datetime.fromtimestamp(timestamp1)


    for x in names:
        vector_names.append(x['name'])

    latitude = str(parametri['latitude']);
    longitude = str(parametri['longitude']);

    distance = haversine(float(latitude), float(longitude));  # Current Coords for ISS
    # http://api.open-notify.org/astros.json shadowUpdate()  - update the device shadow JSON document string from AWS
    # IoT Response from the AWS will be available in the registered callback If no response is received within the
    # provided timeout, a timeout notification will be passed into the registered callback
    informatii = {"state":{"reported":{"iss_position":{"longitude":  longitude, "latitude":\
        latitude,"distance_fromCluj": distance}, "names": vector_names, "currentTime": str(timp_curent) , "number":  n.json()['number']}}};

    myDeviceShadow.shadowUpdate(json.dumps(informatii), myShadowUpdateCallback, 5)
    with open('informatii_ISS.json', 'a') as json_file:
        json.dump(informatii, json_file, indent="\t")
        json_file.write('\n');
    # Wait for values to be added.
    time.sleep(60)
