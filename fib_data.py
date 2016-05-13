'''
Created on Nov 13, 2014

@author: arunjacob
'''
import MySQLdb

import json
import logging
import datetime

logging.basicConfig()

class DataEncoder(json.JSONEncoder):
        
    def default(self,o):
        return o.__dict__
    
fibDataLogger = logging.getLogger('fibdata')
fibDataLogger.setLevel(logging.DEBUG)

class FibData(object):
    '''
    contains fib_id, fib_value, created information.
    '''


    def __init__(self, row = None, details = None):
        


        if row != None:
            fibDataLogger.debug("initializing from database")
            
            self.request_id = row[0]
            self.fib_id = row[1]
            self.fib_value = row[2]
            self.created_date = row[3]
        elif details != None:
            fibDataLogger.debug("initializing from JSON")
            self.request_id = -1
            if details.has_key('fib_id') == True:
                self.fib_id = details['fib_id']
            else:
                fibDataLogger.error("invalid JSON format, sequence_id not found")
                raise 'invalid format'
            
            if details.has_key('fib_value') == True:
                self.fib_value = details['fib_value']
            else:
                fibDataLogger.error("invalid JSON format, sequence_value  not found")
                raise 'invalid format'    
            
            # created is optional. It's always overwritten on insert to db.
            if details.has_key('created_date'):
                self.created_date = details['created_date']
    
    
    
class FibDataDB(object):
    
    def __init__(self,url,dbName,userName,password):
        
        self.log =  logging.getLogger('messageDB')
        self.log.setLevel(logging.DEBUG)
        self.url= url
        self.dbName = dbName
        self.userName = userName
        self.password = password
        
            
    
        
             
    def connectToDB(self):
        try:
            self.log.debug("connecting database")
            db = MySQLdb.connect(host=self.url,user=self.userName,passwd=self.password,db=self.dbName) 
            cur = db.cursor()
            cur.execute('use %s'%self.dbName)
            return db
        except MySQLdb.Error, e:
            self.log.error("unable to connect to database")
            self.handleMySQLException(e,True)
            return None
            
    def createTable(self):
        
        try:
            db = self.connectToDB()
            fibdataTableCreate = 'CREATE TABLE IF NOT EXISTS fibdata( request_id int not null auto_increment, fib_id int not null, fib_value bigint not null, created_date varchar(100), PRIMARY KEY(request_id));'
            
            cur = db.cursor()
    
            self.log.debug('executing fibdata table create')
            
            cur.execute(fibdataTableCreate)
            db.commit()
            self.log.debug('fibdata table created')
            
            self.disconnectFromDB(db)
        
        except MySQLdb.Error, e:
            self.log.error("error creating table fibdata")
            self.handleMySQLException(e,True)
            return None
        
        
    def dropTable(self): 
        try:
            db = self.connectToDB()
            fibdataTableCreate = 'DROP TABLE fibdata'
            
            cur = db.cursor()
    
            self.log.debug('executing fibdata table drop')
            
            cur.execute(fibdataTableCreate)
            db.commit()
            self.debug('fibdata table removed')
            
            self.disconnectFromDB(db)
        
        except MySQLdb.Error, e:
            self.log.error("error removing table fibdata")
            self.handleMySQLException(e,True)
            return None
        
    def disconnectFromDB(self,db):
        try: 
            db.close()
            
        except MySQLdb.Error, e:
            self.log.error("unable to disconnect from database")
            self.handleMySQLException(e,True)
            
            
            
    def handleMySQLException(self,e,throwEx=False):
        """
        parses sql exceptions into readable format
        """
        try:
            self.log.error( "Error [%d]: %s"%(e.args[0],e.args[1]))
        except IndexError:
            self.log.error( "Error: %s"%str(e))
            
        raise e
    
    def addRequest(self,request):
        """
        inserts a request into the database and timestamps it for readability
        """
        try:
            db = self.connectToDB()
            cur = db.cursor()
            #created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            created_date = unicode(datetime.datetime.now())
            self.log.debug("adding request into database with fib_id = %d and fib_value = %d and created_date = '%s'"%(request.fib_id,request.fib_value,created_date))
            query = "insert into fibdata(fib_id, fib_value,created_date) values(%d,%d,'%s')"%(request.fib_id, request.fib_value,created_date)
            cur.execute(query)
            db.commit()
            self.disconnectFromDB(db)
                
                
        except MySQLdb.Error as e:
            self.log.error(str(e))
            self.handleMySQLException(e)
       
       
    def getRequests(self,isDescending=True,limit = 100):
        """
        retrieves specified limit count of messages from database
        """
    
        requests = []
        self.log.debug("retrieving messages, limit = %d"%limit)
        try:
            
            db = self.connectToDB()
            if isDescending == True:
                query = 'select request_id,fib_id, fib_value,created_date from fibdata order by fib_id DESC LIMIT %d'%limit
            else:
                query = 'select request_id,fib_id, fib_value,,created_date from fibdata order by fib_id LIMIT %d'%limit # will order ASC because message_id is the primary key
            
            cur = db.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            
            for row in rows:
                requests.append(FibData(row))
                
            
        except MySQLdb.Error, e:
            self.handleMySQLException(e)
    
        self.disconnectFromDB(db)
        self.log.debug("returning %d request"%len(requests))
        return requests
    

    def dropAllRequests(self):
        """
        for testing: truncate the db
        """
        self.log.debug("dropping all fibdata")
        try:
            db = self.connectToDB()
            query = "TRUNCATE TABLE fibdata"
            cur = db.cursor()
            cur.execute(query)
            db.commit()
            
        except MySQLdb.Error, e:
            self.log.error(str(e))
            self.handleMySQLException(e)
        
        self.disconnectFromDB(db)
            
