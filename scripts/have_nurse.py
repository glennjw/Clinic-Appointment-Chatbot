#!/usr/bin/env python

import sys
import pymysql.cursors
from datetime import datetime


connection = pymysql.connect(host='52.70.223.35',
                             user='clinicuser',
                             password='sparky19',
                             db='ClinicDB')
cursor = connection.cursor()

def search_nurse(target):
    if len(target.split()) == 1:
        sql = "SELECT FirstName, LastName FROM nurses WHERE FirstName = '%s' OR LastName = '%s' "
        cursor.execute(sql % (target, target ))
        sql_result = cursor.fetchall()
    else:
        sql = "SELECT FirstName, LastName FROM nurses WHERE FirstName = '%s' AND LastName = '%s' "
        cursor.execute(sql % (target.split()[0], target.split()[-1] ))
        sql_result = cursor.fetchall()
    sql_result_list = []
    if len(sql_result) == 0:
        return ('No %s found in database.' % target)    
    for i in range(len(sql_result)):
        sql_result_list.append(sql_result[i][0]+ ' ' + sql_result[i][1])
    result = ', '.join(sql_result_list)
    return ('Yes, we have %d : %s' % ( len(sql_result),result ) )

result = search_nurse(sys.argv[1])
print(result)




