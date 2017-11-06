#!/usr/bin/python

import serial
import datetime
import os
import time

record_file = '/home/pi/record'
configuration_file = '/home/pi/config.txt'

alarm_is_activated = False

id_names = {'7689472' : 'buanderie_ext' ,
            '5592405' : 'buanderie_mvt',
            '4117457' : 'telecommande_1_ON',
            '4117458' : 'telecommande_1_OFF',
            '16078080' : 'veranda_ext',
            '1922304' : 'entree',
            '5330389' : 'fenetre_cuisine'
}

id_dates = {'7689472' : '',
            '5592405' : '',
            '4117457' : '',
            '4117458' : '',
            '16078080' : '',
            '1922304' : '',
            '5330389' : ''
}

last_received = {'date' : datetime.datetime(2007, 1,1), 'ID' : ''}

def update_record_file():
  f = open(record_file, 'r')
  f_temp = open(record_file+'_temp', 'w')

  for device in reversed(id_dates.keys()):
     line = f.readline();
     if id_dates[device]!='':
         f_temp.write(id_names[device]+ ' ' + id_dates[device] + '\n')
         id_dates[device]=''
     else:
         f_temp.write(line)
  f.close()
  f_temp.close()
  os.system('mv ' + record_file + '_temp ' + record_file)

def startAlarm():
  global alarm_is_activated
  alarm_is_activated = True
  ser.write("CMD 1981 1\n\r")
  time.sleep(1.5)
  ser.write("CMD 1981 0\n\r")
  time.sleep(1)
  ser.write("CMD 1981 1\n\r")
  time.sleep(1.5)
  ser.write("CMD 1981 0\n\r")
  os.system('echo "ALARM_IS_ACTIVATED = True" > ' + configuration_file)


def stopAlarm():
  global alarm_is_activated
  alarm_is_activated = False
  ser.write("CMD 1981 1\n\r")
  time.sleep(1.5)
  ser.write("CMD 1981 0\n\r")
  os.system('echo "ALARM_IS_ACTIVATED = False" > ' + configuration_file)


def isAlarmActivated():
  previousState = False
  config = open(configuration_file, 'r')
  line = config.readline();
  if ("ALARM_IS_ACTIVATED" in line) and ("True" in line):
    previousState = True
  config.close()
  return previousState
    




ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

if isAlarmActivated():
  startAlarm()

while (1):
  read=ser.readline()
  if 'Received' in read:
    #print read
    for idd in id_dates.keys():
      if idd in read:
        now = datetime.datetime.now();
        #print 'received'
        if not ((now-last_received['date']).seconds<2 and last_received['id']==idd):
            last_received['date']=now
            last_received['id']=idd
            id_dates[idd]=str(now)[:19]
            #print id_dates[idd]
            update_record_file()
            if id_names[idd]=='telecommande_1_ON':
              startAlarm()
            if id_names[idd]=='telecommande_1_OFF':
              stopAlarm()

            if alarm_is_activated:
              if id_names[idd] in ['buanderie_ext', 'buanderie_mvt', 'veranda_ext', 'entree', 'fenetre_cuisine']:
                ser.write("CMD 1981 1\n\r")        
        
