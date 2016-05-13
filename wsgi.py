#!/usr/bin/env python

import os
import bottle
import logging
import urlparse
import uuid
from fib_data import  FibDataDB, DataEncoder, FibData

from bottle import route, get, post, request, template


import json

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

logging.basicConfig()
log = logging.getLogger('receiver')
log.setLevel(logging.DEBUG)


log.debug("setting up db connection...")

try:
    mysql_url = urlparse.urlparse(os.environ['MYSQL_URL'])
except KeyError:
    log.warn("env variable MYSQL_URL not found, reverting to DATABASE_URL")
    mysql_url = urlparse.urlparse(os.environ['DATABASE_URL'])


url = mysql_url.hostname
password = mysql_url.password
user = mysql_url.username
dbname = mysql_url.path[1:] 


fibDataDB = FibDataDB(url,dbname,user,password)

log.debug('generating internal id')

uid = uuid.uuid1()

'''
view routes
'''

@route('/')
def home():
    bottle.TEMPLATE_PATH.insert(0, './views')
    return bottle.template('home')
    
@get('/received') 
def getReceived():
    
    log.debug("handling /received path")
    
    allRequestData = fibDataDB.getRequests()
    
    return json.dumps(allRequestData,cls=DataEncoder)

@get('/instance')
def getInstance():
    log.debug('getting instance id')
    
    instanceId = str(uid)
    
    return "{'instance-id':'%s'}"%instanceId

'''
Fibonacci sequence, recursive
'''

def F(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return F(n-1)+F(n-2)


'''
Control routes
'''
@post('/fib') 
def fib():
    number = request.json['number']
    if not number:
        return template('Please add a number to the end of url: /fib/5')
    fib = F(int(number))
    json_body = json.dumps({'fib_id':int(number), 'fib_value':int(fib)})
    
    requestContents = json.loads(json_body)
    
    requestData = FibData(None,requestContents)
        
    fibDataDB.addRequest(requestData)
    
    return json_body


'''
Adding this route for use with StormRunner (to automate load, compute utilization)
'''

@route('/fib/<number:int>') 
def fib_num(number):
    if not number:
        return template('Please add a number to the end of url: /fib/5')
    fib = F(int(number))
    json_body = json.dumps({'fib_id':int(number), 'fib_value':int(fib)})
    return json_body

'''
required to serve static resources
'''
@route('/static/:filename')
def serve_static(filename):
    log.debug("serving static assets")
    return bottle.static_file(filename, root=STATIC_ROOT)

'''
service runner code
'''
log.debug("starting web server")
application = bottle.app()
application.catchall = False


#UNCOMMENT BELOW FOR RUNNING ON LOCALHOST
#bottle.run(application, host='127.0.0.1', port=8080)

#UNCOMMENT BELOW FOR RUNNING ON HDP
bottle.run(application, host='0.0.0.0', port=os.getenv('PORT', 8080))


# this is the last line
