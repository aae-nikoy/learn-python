import pymssql as ms
import time
import os

class Database(object):
    
    def __init__(self,host,port,user,passwd,database='VM2017'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.database=database
        
    def __conn(self):
        try:
            conn=ms.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,database=self.database)  
        except Exception as e:
            print("连接错误！请检查帐号密码是否正确")
        cur=conn.cursor()
        return cur
    
    def backup(self,path):   #####备份数据
        cur=self.__conn()
        print("连接数据库成功")
        print("开始执行备份操作！")
        cur.execute(''''BACKUP DATABASE "%s" TO DISK ='%s' with init''',(self.database,path))
        print ("备份操作执行完成！")

    def cleanup(path):       #######清理两天前的备份数据
        os.chdir(path)
        for dir,name,file in os.walk(path):
            for i in range(len(file)):
                path=dir+"\\"+file[i]
                file_time=time.localtime(os.path.getctime(path))
                
                if time.localtime()[2]-file_time[2]>0:
                    os.remove(path)

    
while True:
    sql=Database("127.0.0.1","1433","sa","123456")
    year=time.localtime()[0]
    month=time.localtime()[1]
    day=time.localtime()[2]
    if day==1:
        sql.backup("E:\\backup\\%s.bak" % sql.database)
        sql=Database("127.0.0.1","1433","sa","123456","VM2017_his%" %(str(year[2:])+str(month)))
        sql.backup("E:\\backup\\%s.bak" % sql.database)
    else:
        pass

print("test")
