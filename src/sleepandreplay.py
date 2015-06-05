import time
import os
import commands
class ManageMySQL(object):
    openCmd='service mysql start'
    closeCmd='service mysql stop'
    statusCmd='service mysql status'

    def getMySQLstatus(self):
        (status,output)=commands.getstatusoutput(self.statusCmd)
        outputArray=output.split(' ')
        try:
            index=outputArray.index('process')  
            #the output format for running is: mysql start/running, process 4625
            #the output format for not running is: mysql stop/waiting
            return True
        except ValueError:
            return False        
    def closeMySQL(self):
        (status,output)=commands.getstatusoutput(self.closeCmd)
    def openMySQL(self):
        (status,output)=commands.getstatusoutput(self.openCmd)
    def restartMySQL(self):
        status=self.getMySQLstatus()
        if status==True:
            print 'stop mysql !'
            self.closeMySQL()
            print 'start mysql !'
            self.openMySQL()
        else:
            print 'mysql does not start yet!'
            
if __name__=='__main__':
    sleepTimeInSecond=10
    mysql_server_status=False
    mysqlMgr=ManageMySQL()
    
    while True:
        print 'sleep !'
        mysqlMgr.restartMySQL()
        time.sleep(sleepTimeInSecond)