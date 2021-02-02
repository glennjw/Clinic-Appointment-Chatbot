#!/usr/bin/env python
import sys
import pymysql.cursors
from datetime import datetime


connection = pymysql.connect(host='IP',
                             user='user',
                             password='pwd',
                             db='DB')
cursor = connection.cursor()


def timedeltaT(time):
    hour = int(time.total_seconds()/3600)
    minute = str(format(int(time.total_seconds()%60), '02d'))
    if hour > 11:
        time = str(hour - 12) + ':' + minute + ' PM'
    else:
        time = str(hour) + ':' + minute + ' AM'
 
    return time

def whenis(name, recdate):
    recdt = recdate.split()[0][:3] + ' ' + format(int(recdate.split()[1]), '02d')
    rec_dt = datetime.strptime(recdt, '%b %d')
    rec_d = '2019' + format(rec_dt.month, '02d') + format(rec_dt.day, '02d') 
    sql = "SELECT nurse_schedule.SlotDate, nurse_schedule.SlotStart, nurse_schedule.SlotEnd FROM nurse_schedule RIGHT JOIN nurses ON nurse_schedule.NurseID=nurses.id WHERE nurses.FirstName = '%s' AND nurse_schedule.SlotDate = %s "
    cursor.execute(sql % (name, rec_d))
    result = cursor.fetchall()
    if len(result) == 0:
        return ('There is no available hours for %s on that day.' % name) 
    return(timedeltaT(result[0][1])  + ' to ' + timedeltaT(result[0][2]))

result = whenis(sys.argv[1], sys.argv[2])
print(result)





