# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:14:22 2020
主要包括对于网页爬取的基础方法
@author: 王志
"""


import requests
import My_logger
import time
import sys
from requests_toolbelt import SSLAdapter
#定义头部信息
User_Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
test_url="https://www.phbs.pku.edu.cn/2019/seminar_0830/1968.html"
header={'User-Agent':User_Agent}
from selenium import webdriver


##获取真实网页信息
def get_html(url):
    try:
        requests.packages.urllib3.disable_warnings()
        html=requests.get(url,timeout=30,headers=header)
        html.raise_for_status()
        html.encoding=html.apparent_encoding
        content=html.text
        return content       
    except Exception as e:
        My_logger.my_logger.error("访问网址出错{}，请检查后再试".format(url))
        My_logger.my_logger.error(e)
        time.sleep(3)
        sys.exit(0)
   
      
##针对讲座信息，爬取讲座的基础方法
def get_html_withheader(url,header):    
    try:
        requests.adapters.DEFAULT_RETRIES=5
        s=requests.session()
        s.keep_alive=False
        try:
            requests.packages.urllib3.disable_warnings()
            html=s.get(url,timeout=30)            
            html.encoding=html.apparent_encoding
            html.raise_for_status()
        except:
            adapter=SSLAdapter('TLSv1')
            s.mount('https://',adapter)
            html=s.get(url,verify=False,timeout=30,headers=header) 
            html.raise_for_status()
        html.raise_for_status()
        content=html.text
        return content       
    except Exception as e:
        My_logger.my_logger.error("访问网址{}出错header是{}，请检查后再试!".format(url,header))
        My_logger.my_logger.error(e)
        time.sleep(3)
        sys.exit(0)
    return None
  
##获取图片信息，并且写到本地
def get_jpeg_out(url,path):
    try:
        with open(path,"wb") as fout:
            fout.write(requests.get(url).content)
    except Exception as e:
        My_logger.my_logger.error("can not write jpeg to:{},{}!".format(path,e))
        sys.exit(0)
    return
##获取时间戳
def get_time_col(time_a):
    time_str=time.strptime(time_a,"%Y-%m-%d")
    return time.mktime(time_str)
  
  
class web_selenium:
    def __init__(self,name):
        self.name=name
        self.driver=None ##selenimu爬取类的chrome引擎
    
    def test(self):
        self.driver=webdriver.Chrome(executable_path=r'H:/my_code/my_ku/chrome_driver/chromedriver.exe')
        self.driver.get('https://www.jd.com/')
        self.driver.find_element_by_id('key').send_keys('雨季不再来')##在搜索框中输入:雨季不再来
        self.driver.find_element_by_class_name('button').click()##点击搜索
        self.time.sleep(2)##休眠
        #print(self.driver.page_source)##打印页面信息
        return self.driver.page_source
    
    ##注意因为是模拟浏览器，所以不需要header
    def get_source(self,url):
        self.driver=webdriver.Chrome(executable_path=r'H:/my_code/my_ku/chrome_driver/chromedriver.exe')
        self.driver.get(url)        
        time.sleep(2)##休眠       
        return self.driver.page_source

    



