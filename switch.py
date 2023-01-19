import requests
import serial
import time
import platform
import subprocess

# This is the USB port and baud rate of the Arduino Uno
ser = serial.Serial('/dev/ttyACM0', 9600)
url = "http://xxx.xxx.xxx.xxx:8090/door" # replace the x's with your own IP address of the rpi server
ping_ip = "<IP address>.local" # same as IP address of the rpi server

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    
    return subprocess.call(command) == 0

while True:
    response = ping(ping_ip) # server is constantly pinged to make sure it is online
    #print(response)

    if(response):
        page = requests.get(url)
        status_raw = page.text
        status = status_raw[4:5]
        #print(status)

        if(status == '0'):
            ser.write(b'0') # Feeding value of 0 to Arduino
        else:
            ser.write(b'1') # Feeding value of 1 to Arduino
            time.sleep(1)
    else:
        print("No response from server.")
        time.sleep(5)