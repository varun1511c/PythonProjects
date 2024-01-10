'''
Author: venkata varun chowdary kantamneni
File Name: Whatsapp_msg.py
Purpose: Draw a graph for selected commodities in given cities
Revision: 00: import pywhatkit and datetime libs
          01: Specify mobile number (with country code), message and time (hou and min in 24hr format)
        
'''


import pywhatkit
from datetime import datetime

now = datetime.now()

chour = now.strftime("%H")
mobile = input('Enter Mobile No of Receiver : ')
message = input('Enter Message you wanna send : ')
hour = int(input('Enter hour : '))
minute = int(input('Enter minute : '))

pywhatkit.sendwhatmsg(mobile,message,hour,minute)
