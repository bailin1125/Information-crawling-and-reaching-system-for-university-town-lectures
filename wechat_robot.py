# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 00:20:10 2019
主要包括对于微信机器人的相关调用
主要是将功能集成到项目中，给项目增加微信提醒的功能

11.26更新
增加了短信的提醒功能

@author: 王志
"""

from wxpy import *
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import My_logger
##充当聊天机器人的基础类
##单例模式的实现
class my_robot(object):
    _instance=None
    
    def __init__(self,name):
        self.name=name
        self.bot=Bot()
        self.put_target=[] ##发送消息的列表
        self.in_target=[] ##接受消息的好友列表
    ##干扰new的过程实现单例模式
    def __new__(cls,*args,**kw):
        if cls._instance is None:
            cls._instance=object.__new__(cls,*args,**kw)
        return cls._instance
    # ##初始化朋友列表
    # def init_friends(self):
        
        
class my_smtp(object):
    '''
    通过smtp服务器进行发送邮件的功能
    同样在设计中使用单例模式来使用，保证服务的唯一存在
    
    '''
    _instance=None
    sender = '1040493601@qq.com'    
    receivers = '1801213262@pku.edu.cn'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #receivers = '2262290472@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    smtp="svagwjhtpujhbbge"
    ##有关发送邮件的配置参数
    subject=r"❤白霖给宝宝的讲座通知❤"
    
    nickname="御用讲座小助手V1.0"  
    def __init__(self): 
        self.name="" ##名字
        self.receivers=[]
        pass
    
    ##单例模式的初始化设置
    def init(self,name):
        self.name=name       
        return
    
    def __new__(cls,*args,**kw):
        if cls._instance is None:
            cls._instance=object.__new__(cls,*args,**kw)
        return cls._instance
    
    @classmethod
    def build_message(my_smtp,all_object):
        '''        
        Parameters：所有的讲座类
        ----------
        Returns：邮件的内容，html格式.

        '''       
        ##首先构建这个邮件的主体
        msgRoot = MIMEMultipart('mixed')
        msgRoot['From'] = Header(my_smtp.nickname, 'utf-8')
        msgRoot['To'] =  Header(my_smtp.receivers, 'utf-8')
        subject = my_smtp.subject
        msgRoot['Subject'] = Header(subject, 'utf-8')
 
        ##构建邮件头
        test_ext="讲座通知邮件"
        msg_text=MIMEText(test_ext,"plain","utf-8")        
        msgRoot.attach(msg_text)
        mail_msg=""
        
        ##获得相关的讲座的数目
        ##发送邮件的要求是，此次是内容是有效的，并且之前没有落库（之前没发现过）
        count=0
        for singel in all_object:
            if(singel.valid==True and singel.this_new==True and singel.right==True):
                count+=1
        if(count==0):
            mail_msg="<p>  可惜了……经过讲座小助手的辛勤劳动，没有发现近期有与宝宝的相关讲座……o(╥﹏╥)o:</p>\n"
            return mail_msg,True
        mail_msg = "<p>   经过讲座小助手的辛勤劳动ヾ(◍°∇°◍)ﾉﾞ，一共发现了";
        mail_msg+=str(count)+"场讲座可能与宝宝有关哦，下面是他们的标题和连接哦(*^▽^*)"+"</p>\n"
        
        ##正式开始组建邮件的正文
        count=0
        real_count=0
        try:
            for singel in all_object:
                if(singel.valid==False or singel.this_new==False or singel.right==False):
                    continue
                title="<p>"+str(real_count+1)+":"+singel.name+"</p>\n"
                real_count+=1
                mail_msg+=title
                mail_msg+="<p><a href="
                url_path='"'+singel.url+'"'+">讲座链接</a></p>\n"
                mail_msg+=url_path
                if(len(singel.jpeg_real_path)!=0):
                    ##默认这里只是放入第一张照片
                    img_path="<p><img src="+'"'+"cid:image"+str(count)+'"'+"></p>\n"
                    mail_msg+=img_path
                    #读取图片
                    with open(singel.jpeg_real_path[0],"rb") as fp:                        
                         msgImage = MIMEImage(fp.read())
                    img_name="'<image"+str(count)+">'"
                    msgImage.add_header('Content-ID', img_name)
                    count+=1
                    msgRoot.attach(msgImage)    
        except Exception as e:
            My_logger.my_logger.error("构造邮件正文遇到问题，退出！")
            My_logger.my_logger.error(e)
            return msgRoot,False
        ##组建html
        msgRoot.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        return msgRoot,True

    ##发送目标邮件，输入是一些列讲座的题目
    def send_mail(self,message):
        ret=True   
     ##定义图片 ID，在 HTML 文本中引用
        try:           
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_smtp.sender, my_smtp.smtp)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_smtp.sender,my_smtp.receivers,message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接     
            print("发送邮件成功！")
        except Exception as e:
            ret=False
            My_logger.my_logger.error("发送邮件：{}失败！".format(my_smtp.subject))
            My_logger.my_logger.error(e)        
        return ret
     
    def singel_test(self):         
        ret=True
        try:
            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
            msg=MIMEText('测试的邮件','plain','utf-8')
            msg['From']=formataddr(["FromRunoob",my_smtp.sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["FK",my_smtp.receivers])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']=my_smtp.subject             # 邮件的主题，也可以说是标题
 
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_smtp.sender, my_smtp.smtp)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_smtp.sender,[my_smtp.receivers,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            My_logger.my_logger.error("发送邮件：{}失败！".format(my_smtp.subject))
            My_logger.my_logger.error(e)
            ret=False
        return ret
    
    
   

class message(object):
    def __init__(self,name):
        self.name=""
        self.content=[] ##发送的列表
        self.title="" ##发送短信的标题
        
class my_message(object):
    '''
    一个自制的短信发送对象
    用来发送指定的短信给用户
    依然需要全局单例模式
    '''
    _instance=None
    def __init__(self,name):
        self.name=name
        
    def __new__(cls,*args,**kw):
        if cls._instance is None:
            cls._instance=object.__new__(cls,*args,**kw)
        return cls._instance
    def texting(self,messge):
        return None
        
    
    
            
    