from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import random
import serial
import os
import RPi.GPIO as GPIO

raspberryPi = False
if (os.path.exists('/dev/ttyS0')):
    raspberryPi = True
    print('Find serial port at /dev/ttyS0')
else:
    print('Can not find serial port at /dev/ttyS0')
if (raspberryPi):
    ser = serial.Serial('/dev/ttyS0', baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS
                    )
    AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    # print("Received a new message " + "from topic: " + message.topic)
    obj = json.loads(message.payload)
    # print(message.payload)
    if (raspberryPi):
        if ('command_angle1' in obj):
            angle1 = obj['command_angle1']
            angle2 = obj['command_angle2']
            angle3 = obj['command_angle3']
            angle4 = obj['command_angle4']
            angle5 = obj['command_angle5']
            angle6 = obj['command_angle1']
            angle7 = obj['command_angle1']
            ser.write('B\n')
            ser.write(str(angle1) + '\n')
            ser.write(str(angle2) + '\n')
            ser.write(str(angle3) + '\n')
            ser.write(str(angle4) + '\n')
            ser.write(str(angle5) + '\n')
            ser.write(str(angle6) + '\n')
            ser.write(str(angle7) + '\n')
            ser.write('E\n')
    print(obj['text'])
    if ('command_angle1' in obj):
        print(int(int(obj['command_angle1'])/2))
        p.ChangeDutyCycle(int(int(obj['command_angle1'])/2))
        print('angle1: ' + str(obj['command_angle1']))
    if ('command_angle2' in obj):
	    print('angle2: ' + str(obj['command_angle2']))
    if ('command_angle3' in obj):
	    print('angle3: ' + str(obj['command_angle3']))
    if ('command_angle4' in obj):
	    print('angle4: ' + str(obj['command_angle4']))
    if ('command_angle5' in obj):
	    print('angle5: ' + str(obj['command_angle5']))
    print("--------------")


# Read in command-line parameters
# parser = argparse.ArgumentParser()
# parser.add_argument("-e", "--endpoint", action="store", dest="host", help="Y`our AWS IoT custom endpoint`")
# parser.add_argument("-r", "--rootCA", action="store", dest="rootCAPath", help="Root CA file path")
# parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
# parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
# parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
#                     help="Use MQTT over WebSocket")
# parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
#                     help="Targeted client id")
# parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
# parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
#                     help="Operation modes: %s"%str(AllowedActions))
# parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World from Server!",
#                     help="Message to publish")
# args = parser.parse_args()
# host = 'a21zozqgendyv9.iot.us-east-2.amazonaws.com'
# rootCAPath = '~/.aws/root-CA.crt'
# certificatePath = '~/.aws/465eb4c119-certificate.pem.crt'
# privateKeyPath = '~/.aws/465eb4c119-private.pem.key'
host = 'a21zozqgendyv9.iot.us-east-2.amazonaws.com'
rootCAPath = 'root-CA.crt'
certificatePath = 'certificate.pem.crt'
privateKeyPath = 'private.pem.key'
useWebsocket = False
clientId = 'iot' + str(int(random.random()*10000000000000))
print('clintId: ' + clientId)
topic = 'oparp'
mode = 'both'
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 200)
p.start(1)
# if args.mode not in AllowedActions:
#     parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
#     exit(2)

# if args.useWebsocket and args.certificatePath and args.privateKeyPath:
#     parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
#     exit(2)

# if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
#     parser.error("Missing credentials for authentication.")
#     exit(2)

# Configure logging
# logger = logging.getLogger("AWSIoTPythonSDK.core")
# logger.setLevel(logging.DEBUG)
# streamHandler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if mode == 'both' or mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    if mode == 'both' or mode == 'publish':
        message = {}
        message['message'] = 'oparp'
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        # myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
    time.sleep(1)
