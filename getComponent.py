#!/usr/bin/python

from MySQLdb import connect as mysql_connect
from json import dumps as json_dumps
from cgi import parse_qs, escape

from settings import database

#
# WSGI entry point
#
def application(environ, start_response):

    # HTTP response stats will always be OK, errors are be reported as JSON
    start_response('200 OK', [('Content-Type', 'text/html'), ('Access-Control-Allow-Origin', '*')])
    
    # parse query string
    arg = parse_qs(environ['QUERY_STRING'])
    id = arg.get('ID', [''])[0]

    # only allow integers as ID: avoid code injection
    try:
        int(id)
    except:
        return '{ "error": "Invalid query string" }'

    # connect to MySQL database
    mysql = mysql_connect(database['host'], database['user'], database['pw'], database['db'])
    cursor = mysql.cursor()
    
    # request component from database
    cmd = "SELECT ID,Developer,Model FROM `Components` WHERE `ID`="+id+";"
    cursor.execute(cmd)
    row = cursor.fetchone()
    
    # component not found
    if row is None:
        return '{ "error": "Component not found in database" }'

    # return result as JSON
    result = {
                'ID':        str(row[0]),
                'Developer': row[1],
                'Model':     row[2]
             }
    return json_dumps(result, indent=4)

#
# If invoked from console
#
if __name__ == "__main__":
    def dummy_callback(a, b):
        return
    application("", dummy_callback)
