import time
import serial
import random
print "Starting program"
ser = serial.Serial('/dev/ttyS0', baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS
                    )

try:
    print 'Starting sending data from uart.'
    while True:
        time.sleep(1)
        # angle1 = random.random() + 1
        # angle2 = random.random() + 2
        # angle3 = random.random() + 3
        # angle4 = random.random() + 4
        # angle5 = random.random() + 5
        # angle6 = random.random() + 6
        # angle7 = random.random() + 7
        angle1 = 1
        angle2 = 2
        angle3 = 3
        angle4 = 4
        angle5 = 5
        angle6 = 6
        angle7 = 7
        ser.write('B\n')
        ser.write(str(angle1) + '\n')
        ser.write(str(angle2) + '\n')
        ser.write(str(angle3) + '\n')
        ser.write(str(angle4) + '\n')
        ser.write(str(angle5) + '\n')
        ser.write(str(angle6) + '\n')
        ser.write(str(angle7) + '\n')
        ser.write('E\n')
        if ser.inWaiting() > 0:
            data = ser.readline()
            print data

except KeyboardInterrupt:
    print "Exiting Program"

except:
    print "Error Occurs, Exiting Program"

finally:
    ser.close()
    pass
