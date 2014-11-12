#!/usr/bin/python

from MySQLdb import connect as mysql_connect
from json import dumps as json_dumps
from settings import database

#
# WSGI entry point
#
def application(environ, start_response):

    # connect to MySQL database
    mysql = mysql_connect(database['host'], database['user'], database['pw'], database['db'])
    cursor = mysql.cursor()
    cmd = "SELECT ID,Developer,Model FROM `Components` WHERE `ID`=1;"
    cursor.execute(cmd)
    row = cursor.fetchone()
    result = {
                'id':        row[0],
                'developer': row[1],
                'model':     row[2]
             } 
  
    start_response('200 OK', [('Content-Type', 'text/html')])
    return json_dumps(result, indent=4)

#
# If invoked from console
#
if __name__ == "__main__":
    def dummy_callback(a, b):
        return
    application("", dummy_callback)
