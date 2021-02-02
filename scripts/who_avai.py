#!/usr/bin/env python

import sys
import pymysql.cursors
from datetime import datetime


connection = pymysql.connect(host='IP',
                             user='user',
                             password='pwd',
                             db='DB')
cursor = connection.cursor()

def whois(rectime, recdate):
    recdt = recdate.split()[0][:3] + ' ' + format(int(recdate.split()[1]), '02d')  + ' ' + format(int(rectime.split()[0]), '02d')  + ' ' + rectime.split()[1]
    rec_dt = datetime.strptime(recdt, '%b %d %I %p')
    if rec_dt.hour < 9 or rec_dt.hour > 16:
        return "Sorry, it's out of hours"
    rec_t = format(rec_dt.hour, '02d') + '0000'
    rec_d = '2019' + format(rec_dt.month, '02d') + format(rec_dt.day, '02d')
    sql = "SELECT nurses.FirstName, nurses.LastName FROM nurse_schedule LEFT JOIN nurses ON nurse_schedule.NurseID=nurses.id WHERE nurse_schedule.SlotStart <= %s AND nurse_schedule.SlotEnd - 1 >= %s AND nurse_schedule.SlotDate = %s "
    cursor.execute(sql % (rec_t, rec_t, rec_d))
    sql_result = cursor.fetchall()
    if len(sql_result) == 0:
        return ('Sorry, no nurse is available at that time.')
    sql_result_list = []
    for i in range(len(sql_result)):
        sql_result_list.append(sql_result[i][0]+ ' ' + sql_result[i][1])
    result = ', '.join(sql_result_list) 
    return result

result = whois(sys.argv[1], sys.argv[2])
print(result)





