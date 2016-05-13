'''
Created on Nov 14, 2014

@author: arunjacob
'''
import unittest
import urlparse
import os

from fib_data import FibData, FibDataDB
from test_utils import initializeDB
import datetime
import MySQLdb

class Test(unittest.TestCase):


    def setUp(self):
        
        try:
            # create a test database.
            self.testName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            MYSQL_URL = "mysql://dev:devpass@localhost/test"
            
            mysqlUrl = urlparse.urlparse(MYSQL_URL)
            url = mysqlUrl.hostname
            password = mysqlUrl.password
            userName = mysqlUrl.username
            dbName = mysqlUrl.path[1:] # slice off the '/'
            
            db = MySQLdb.connect(host=url,user=userName,passwd=password,db=dbName) 
            cur = db.cursor()
            cur.execute('create database %s'%self.testName)
            db.commit()
            
            #cur.execute("GRANT ALL ON %s.* TO 'dev'@'localhost';"%self.testName)
            #db.commit()
            fibDataDB = FibDataDB(url, self.testName,userName,password)
            
            fibDataDB.createTable()
            db.commit()
            
            db.close()
        except MySQLdb.Error, e:
            self.log.error("error creating table fibdata")
            self.log.error(e)
            self.handleMySQLException(e,True)
            return None        
        
    def test1InitializeMessage(self):
        
        fibDataDB = initializeDB()
        fibData = FibData(None,{"fib_id":3, "fib_value":2})
        fibDataDB.addRequest(fibData)

        reqs = fibDataDB.getRequests()
        
        self.assertTrue(reqs != None)

        self.assertTrue(len(reqs) > 0)
        
        
    def test2DropAllRequests(self):
        fibDataDB = initializeDB()
        fibDataDB.dropAllRequests()
        
    def tearDown(self):
        try:
            MYSQL_URL = "mysql://dev:devpass@localhost/test"
            
            mysqlUrl = urlparse.urlparse(MYSQL_URL)
            url = mysqlUrl.hostname
            password = mysqlUrl.password
            userName = mysqlUrl.username
            dbName = mysqlUrl.path[1:] # slice off the '/'
            
            db = MySQLdb.connect(host=url,user=userName,passwd=password,db=dbName) 
            cur = db.cursor()
            
            cur.execute('drop database %s'%self.testName)
            db.commit()
            db.close()
        except MySQLdb.Error, e:
            self.log.error("error removing table fibdata")
            self.handleMySQLException(e,True)
            return None
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()