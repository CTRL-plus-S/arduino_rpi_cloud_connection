'''
In this file we establish connection between raspberry pi and
radio receiver module attached to its usb port. The telemetry
wirelessly is sent by a micro station will be received by antena
of RPi and is read & saved in CSV file by the script below.

Telemetry line example: $ 2233, 454, 45, 87, 69, 49.4545,  45.5879, 03-07-2020_12-52-14-234 !
                        $ ms-id, s1, s2, s3, s4, gps-lat, gps-long, dd-mm-yyyy_hh-mm-ss-msc !
'''
import requests, csv, serial, time
url = 'http://ptsv2.com/t/rotq3-1593869400/post' # MUST be changed to actual cloud url

try:
    # setting csv write file:
    csvfile = open('telemetry.csv', 'w', newline='')
    csvwriter = csv.writer(csvfile)
except:
    print("Error occured in creating and opening CSV file")

try:
    # setting serial port:
    ser = serial.Serial('/dev/ttyACM0', 9600) # choose radio device, set baudrate
    data = ser.read().decode('utf-8') # read first input
except:
    print("Error in finding the device or connecting to it")

try:
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
        # print(telemetry)

        # Getting the photo to POST it 
        image = open('photo-03-07-2020_12-52-14-234_2233.txt', 'rb')
        files = {'image': image}

        #POST the telemetry & image to the cloud url
        req_try_count = 0
        while(req_try_count <= 5):
            response = requests.post(url, data={'telemetry': telemetry}, files=files)
            req_try_count += 1
            if(response.status_code == 200): # 200 -> OK
                break
            else:
                time.sleep(0.5)
        
        #write to csv file
        datas = telemetry[1:-2].split(',')
        csvwriter.writerow(datas)

    csvfile.close()
except:
    csvfile.close()
    print("The program is terminated with error, but didn't crush")
    print("The received telemetries are saved in the CSV file successfully!")
