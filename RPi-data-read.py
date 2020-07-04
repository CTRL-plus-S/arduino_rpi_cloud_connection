'''
In this file we establish connection between raspberry pi and
radio receiver module attached to its usb port. The telemetry
wirelessly is sent by a micro station will be received by antena
of RPi and is read & saved in CSV file by the script below.
'''

import serial
# telemetry line example: $ 2233, 454, 45, 87, 69, 49.4545,  45.5879 !
#                         $ ms-id, s1, s2, s3, s4, gps-lat, gps-long !

ser = serial.Serial('/dev/ttyACM0', 9600) # choose device, set baudrate
data = ser.read().decode('utf-8') # read first input

# Main telemmetry loop
while(data):
    # To find the beginning of telemetry, i.e. '$'
    while(data != '$'):
        data = ser.read().decode('utf-8')

    # Collect the telemetry line, ends with '!'
    telemetry = ''
    while(data != '!'):
        telemetry += data
        data = ser.read().decode('utf-8')
    telemetry += data # make sure the last char, i.e '!' is added
        
    print(telemetry)
