# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:53:20 2020
相关的运行参数，读取配置文件之后返回其他数值，供其他模块调用
@author: 王志
"""



import configparser
import My_logger
import time
import os
cf=configparser.ConfigParser()
user_name=""; ##用户名
passwd=""; ##密码
org_path=""; ##原始路径，用于输出等
hit_flag=""; ##是否读取hit的相关讲座信息
tsinghua_flag=""; ##是否读取清华的讲座信息
stl_flag=""; ##是否读取国法的相关讲座
hsbc_flag=""; ##是否读取汇丰的相关讲座
utsz_flag="";
#文件夹不可存在的符号
error_key=['\\',r'/',r':','*',"?",r'"',r"<",r">",r"|",r".",r"|",r"？",r"?"]


##访问时候相关参数
#定义头部信息
User_Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
Referer={"HSBC":"https://www.phbs.pku.edu.cn/",
         "STL":"http://stl.pku.edu.cn/",
         "TSINGHUA":"https://www.sigs.tsinghua.edu.cn/",
         "HIT":"http://www.hitsz.edu.cn/article/id-78.html",
         "utsz_lecture":"https://lib.utsz.edu.cn/media/css/style.css"}

Host={"HSBC":"www.phbs.pku.edu.cn",
      "STL":"stl.pku.edu.cn",
      "TSINGHUA":"www.sigs.tsinghua.edu.cn",
      "HIT":"www.hitsz.edu.cn",
      "utsz_lecture":"lib.utsz.edu.cn"}

##讲座有效性的判断
Seminar_valid_list=["电子信息","人工智能","图像识别"]

##讲座的index的url
HSBC_seminar="https://www.phbs.pku.edu.cn/about/Allnews/seminar/index.html"
law_school_url="https://stl.pku.edu.cn/category/events/"
TSINGHUA_url="https://www.sigs.tsinghua.edu.cn/xs_2578/list.htm"
HIT_url="http://www.hitsz.edu.cn/article/id-78.html"
utsz_lecture_url="https://lib.utsz.edu.cn/activity/id-687.html?locale=zh_CN"
##初始化函数，用以读取相关参数
def init():
    try:        
        cf.read("config.ini",encoding='utf-8')
        user_name=cf.get("user","name")
        passwd=cf.get("user","passwd")
        global org_path
        global hit_flag
        global tsinghua_flag
        global stl_flag
        global hsbc_flag
        global utsz_flag
        org_path=cf.get("user","path")
        hit_flag=cf.get("falg","HIT")
        tsinghua_flag=cf.get("falg","TSINGHUA")
        stl_flag=cf.get("falg","STL")
        hsbc_flag=cf.get("falg","HSBC")  
        utsz_flag=cf.get("falg","utsz")
    except Exception as e:        
        My_logger.my_logger.eror("配置文件读取异常，请检查后重试（程序2s后退出）")
        My_logger.my_logger.error(e)
        time.sleep(2)
        os.exit(0)
    
    #这样说明读取配置文件成功
    if(passwd!="521521"  or user_name!="chenhuan"):
        print("账号或者密码错误，您不被授权使用本程序，即将关闭")
        My_logger.my_logger.error("被禁止使用本程序，请检查")
        time.sleep(5)
        os.exit(0) 
    My_logger.my_logger.info("读取配置文件成功！")    
    My_logger.my_logger.info("感谢用户{}使用本程序。".format(user_name))
    return
  
  
##判断某个字符串是不是符合要求
def judge_str(input):
    if(len(str(input))==0):
        return False
    if(str(input) is not None and str(input) !=" "  and  str(input)!='\xa0' and not("nbsq" in str(input))):
        return True


##对列表进行字符串替换，替换掉非法的字符
def replace_valid_str(input):
    after_list=[]
    for title in list(input):
        title=title.strip()
        for error in error_key:
            if(error in title):
                title=title.replace(error,"") 
        after_list.append(title)            
    return after_list