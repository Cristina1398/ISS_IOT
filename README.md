# ISS_IOT
The Python file will get information from the API http://api.open-notify.org/iss-now.json which return the current location of the ISS (Internation Space Station).
AWSIoTMQTTShadowClient is the client class used for device shadow operations with AWS IoT. It has a method shadowUpdate() for updating the device shadow. 
The connection with AWS will be made through private keys and certificates. 
These information from API will be send to AWS where will be displayed using a serviced named QuickSight.A message will be sent if a certain distance 
from Cluj has been exceeded. For the notification purpose it was used Amazon Simple Notification Service (Amazon SNS).
