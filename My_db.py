# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 00:21:22 2020


一些落库的相关逻辑
通过1433端口，链接同一个子网下面的服务器
在业务行为中进行增删改查的操作

@author: 王志
"""
import My_logger
import pymssql
import inspect
target_ip="10.113.55.86"  ##服务器ip
port="1433"  ##服务器端口
account="wangz"  ##用户名
passwd="ab82808976"  ##密码
DB_name="Poster"  ##数据库名
table_name="poster_get" ##数据的表名




class table_data(object):
    """
    数据库中数据表一行数据的抽象
    """
    def __init__(self):
        self.id=0 ##储存的id主键
        self.name=""
        self.url=""
        self.time=""
        self.real_time=""
        self.type="" ##这个讲座的类别
        self.if_file=False ##是否落到本地了
        self.if_post=False ##
    ##将seminar类转变为data类
    ##为了保证模块之间的松耦合性，这里采用反射方法获取信息
    @classmethod
    def seminar2data(table_data,seminar):
        dirr=inspect.getmembers(seminar)
        #print(dirr[2][1])
        res=table_data()
        res.name=dirr[2][1]["name"]
        res.url=dirr[2][1]["url"]
        res.time=dirr[2][1]["time"]
        res.real_time=dirr[2][1]["real_time"]
        res.type=dirr[2][1]["type"]
        res.if_file=dirr[2][1]["tofile"]
        res.if_post=dirr[2][1]["valid"]
        return  res

class my_db(object):
    """
    为了方便数据库的交互所做的相关操作
    与主机的sql数据库进行增删改查
    依然是单例模式
    """
    instance=None    
    def __init__(self):
        self.name="db"
        self.conn=None
        self.cursor=None
        return
    def __new__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance=object.__new__(cls,*args,**kw)
        return cls.instance
    ##为数据库建立链接
    def get_conn(self):
        try:
            self.conn = pymssql.connect(target_ip, account, passwd, DB_name)
            self.cursor = self.conn.cursor()
        except Exception as e:
            My_logger.my_logger.error("无法获得数据库的连接！")
            My_logger.my_logger.error(e)
        return
    

    ##查找操作，查找title对应的记录        
    def select_save_by_name(self,name):
        # 查询操作
        com="SELECT * FROM {} WHERE name=%s".format(table_name)
        forma=name
        target=[]
        self.cursor.execute(com,forma)
        self.conn.commit()
        row = self.cursor.fetchone()
        while row:
            temp=table_data()
            temp.id=row["id"]
            temp.name=row["name"]
            temp.url=row["url"]
            temp.time=row["time"]
            temp.real_time=row["real_time"]
            temp.type=row["type"]
            temp.if_file=(str(row[6])=="1")
            temp.if_post=(str(row[7])=="1")            
            print("ID=%d, Name=%s" % (row[0], row[1]))
            row = self.cursor.fetchone()
            target.append(temp)
        return target
    
    def insert_save(self,table_data):
        com="INSERT INTO {} VALUES (%s,%s,%s,%s,%s,%d,%d)".format(table_name)
        form=(table_data.name,table_data.url,table_data.time,table_data.real_time,table_data.type
              ,table_data.if_file,table_data.if_post)
        try:
            self.cursor.execute(com,form)
            # 如果没有指定autocommit属性为True的话就需要调用commit()方法
            self.conn.commit()
        except Exception as e:            
            My_logger.my_logger.error("插入数据遇到问题！继续插入下一条\n")
            My_logger.my_logger.error(e)
       # row = self.cursor.fetchall()
        return 
    
    def close(self):  
        # 关闭连接
        self.conn.close()
        return

    def singel_test(self):
        com="INSERT INTO poster_get VALUES  (%s,%s,%s,%s,%s,%d,%d)"
        forma=("a","b","c","d","e",0,0)       
        try:
            self.cursor.execute(com,forma)
            # 如果没有指定autocommit属性为True的话就需要调用commit()方法
            self.conn.commit()
            self.close()
            return
        except Exception as e:
            self.close()
            My_logger.my_logger.error("插入数据遇到问题！\n")
            My_logger.my_logger.error(e)
       

        