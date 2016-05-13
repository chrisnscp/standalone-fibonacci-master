'''
Created on Sep 4, 2014

@author: jacoba
'''
import MySQLdb
import urlparse
import os
import logging
from fib_data import FibDataDB
if __name__ == '__main__':
    
    try:
        logging.basicConfig()
        log = logging.getLogger('fibonacci')
        log.setLevel(logging.DEBUG)

        try:
            mysql_url = urlparse.urlparse(os.environ['MYSQL_URL'])
        except KeyError:
            log.warn("env variable MYSQL_URL not found, reverting to DATABASE_URL")
            mysql_url = urlparse.urlparse(os.environ['DATABASE_URL'])
    
        #rdb = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        
        url = mysql_url.hostname
        password = mysql_url.password
        userName = mysql_url.username
        dbName = mysql_url.path[1:] # slice off the '/'
        
        fibdataDB = FibDataDB(url,dbName,userName,password)
        
        fibdataDB.createTable()

    except MySQLdb.Error, e:
        print "Exception during database initialization: %s"%str(e)
