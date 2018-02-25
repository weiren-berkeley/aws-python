import time
import serial
print "Starting program"
ser = serial.Serial('/dev/ttyS0', baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
time.sleep(1)
try:
    ser.write('Hello World\r\n')
    ser.write('Serial Communication Using Raspberry Pi\r\n')
    ser.write('By: Wei Ren\r\n')
    print 'Data Echo Mode Enabled'
    while True:
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
