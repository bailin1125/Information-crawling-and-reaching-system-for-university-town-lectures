# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 22:37:27 2019

@author: 王志
"""

#为新媒体而做，爬取指定网页的
import sys
sys.path.append(r"H:\my_code\some_programs\Poster_and_contact")
sys.path.append(r"H:\my_code\some_programs\Poster_and_contact\Seminar")
import supports_seminar as supports
import os
import My_logger
import util
import wechat_robot
import My_db
#定义几个需要的url 
test_url="http://stl.pku.edu.cn/zh-hans/%e6%96%b0%e9%97%bb%e4%b8%ad%e5%bf%83/%e3%80%90%e5%88%86%e4%ba%ab%e4%bc%9a%e9%a2%84%e5%91%8a%e3%80%916%e6%9c%8820%e6%97%a5%ef%bc%88%e5%91%a8%e5%9b%9b%ef%bc%89%ef%bc%9a2019%e5%b1%8a%e6%af%95%e4%b8%9a%e7%94%9f%e5%ae%9e%e4%b9%a0%e5%b0%b1/"

hsbc_path="";
STL_path="";
TSINGHUA_path="";
HIT_path="";
utsz_lecture_path="";







##开始搜寻讲座信息
def find_seminaer():
    ##储存的所有的讲座信息类
    after_list=[]
    
    
    ##1 对汇丰的所有讲座进行处理
    if(util.hsbc_flag=="1"):    
        ##先建立hsbc的文件夹
        global hsbc_path
        hsbc_path=util.org_path+"HSBC/"
        supports.seminar.mkdirs(hsbc_path)
        My_logger.my_logger.info("开始爬取汇丰讲座的全部信息")
        hsbc_time_list,hsbc_url_list,hsbc_title_list=supports.get_HSBC_SEMINAR(util.HSBC_seminar)
        hsbc_title_list=util.replace_valid_str(hsbc_title_list)
        
        ##循环获得每一个的对象
        for i in range(len(hsbc_title_list)):
            after_list.append(supports.get_HSBC_onehtml(hsbc_url_list[i],hsbc_time_list[i],hsbc_path+"/"+hsbc_title_list[i],0))
        My_logger.my_logger.info("汇丰所有讲座信息完成")

    ##2 然后是国法的处理
    if(util.stl_flag=="1"):
        global STL_path
        STL_path=util.org_path+"STL//"
        ##建立国法的储存路径
        supports.seminar.mkdirs(STL_path)
        My_logger.my_logger.info("开始爬取国际法学院讲座的全部信息")
        STL_url_list,STL_title_list,STL_info_list=supports.get_STL_SEMINAR(util.law_school_url)
        STL_title_list=util.replace_valid_str(STL_title_list)
        ##循环获得每一个对象
        for i in range(len(STL_title_list)):
            after_list.append(supports.get_STL_one_html( STL_url_list[i],STL_info_list[i],STL_path+"/"+STL_title_list[i],0))
        My_logger.my_logger.info("国际法学院所有讲座信息完成")

    
    ##3 爬取清华深研院全部讲座    
    if(util.tsinghua_flag=="1"):
        My_logger.my_logger.info("开始爬取清华深研院讲座的全部信息")
        TSINGHUA_url_list,TSINGHUA_title_list,TSINGHUA_time_list=supports.get_TSINGHUA_SEMINAR(util.TSINGHUA_url)
        TSINGHUA_title_list=util.replace_valid_str(TSINGHUA_title_list)
        global TSINGHUA_path
        TSINGHUA_path=util.org_path+"TSING_HUA//"
        ##建立清华的储存文件夹
        supports.seminar.mkdirs(TSINGHUA_path)   
        ##循环每一个讲座信息
        for i in range(len(TSINGHUA_url_list)):            
            after_list.append(supports.get_TSINGHUA_one_html( TSINGHUA_url_list[i],TSINGHUA_time_list[i],TSINGHUA_path+"/"+TSINGHUA_title_list[i],0))
        My_logger.my_logger.info("清华深研院所有讲座信息完成")



    ## 4 爬取哈工大讲座信息    
    if(util.hit_flag=="1"):
        My_logger.my_logger.info("开始爬取哈工大讲座的全部信息")
        HIT_url_list,HIT_titel_list,HIT_real_list,HIT_time_list=supports.get_HIT_SEMINAR(util.HIT_url)
        HIT_titel_list=util.replace_valid_str(HIT_titel_list)
        global HIT_path
        HIT_path=util.org_path+"HIT//"
        ##建立哈工大存储路径
        supports.seminar.mkdirs(HIT_path)
        ##开始循环产生讲座信息
        for i in range(len(HIT_url_list)):           
            after_list.append(supports.get_HIT_one_html( HIT_url_list[i],HIT_titel_list[i],HIT_real_list[i],HIT_time_list[i],HIT_path+"/"+HIT_titel_list[i],0))
        My_logger.my_logger.info("哈工大所有讲座信息完成")

   
    ## 5 爬取大学城发讲座的信息
    if(util.utsz_flag=="1"):
        My_logger.my_logger.info("开始爬取大学城讲座的全部信息")
        utszlecture_url_list,utszlecture_titel_list,utszlecture_info_list,utsz_real_time_list=supports.get_utszlecture_SEMINAR(util.utsz_lecture_url)
        utszlecture_titel_list=util.replace_valid_str(utszlecture_titel_list)
        global utsz_lecture_path
        utsz_lecture_path=util.org_path+"//utsz"
        supports.seminar.mkdirs(utsz_lecture_path)    
        for i in range(len(utszlecture_url_list)):
            after_list.append(supports.get_utszlecture_one_html( utszlecture_url_list[i],utszlecture_titel_list[i],utsz_real_time_list[i],utsz_lecture_path+"/"+utszlecture_titel_list[i],0))
        My_logger.my_logger.info("大学城所有讲座信息完成")
    My_logger.my_logger.info("已经爬取要求的讲座信息")
    print("请到{}下查看下载的相关图片文件".format(util.org_path))    
    return after_list





##对讲座信息进行甄别和判断
##策略是查看讲座的题目
def judge_seminar(after_list):
    for singel in after_list:
        singel.valid=supports.seminar.judge_valid(singel)
    return

##持久化到本地
def toreal_file(after_list):
    for singel in after_list:
        if(singel.type=="utsz"):
            singel.content2file(utsz_lecture_path)
        elif(singel.type=="STL"):
            singel.content2file(STL_path)
        elif(singel.type=="HSBC"):
            singel.content2file(hsbc_path)
        elif(singel.type=="HIT"):           
            singel.content2file(HIT_path)
        else:
            singel.content2file(TSINGHUA_path)
    return

##落库
def alltoDB(after_list):
    ##首先初始化数据库连接
    db=My_db.my_db()
    db.get_conn()    
    ##首先走一个测试
    #db.singel_test()
    ##每次落库前都要检查是否有重复的数据
    for singel in after_list:  
        if(singel.tofile==True and singel.right==True):
            target=db.select_save_by_name(singel.name)
            if(target is  None or len(target)==0):
                test_data=My_db.table_data.seminar2data(singel)
                db.insert_save(test_data)
                singel.this_new=True
            else:
                My_logger.my_logger.info("讲座信息:{}已经落库!".format(singel.name))
                singel.this_new=False
    db.close()
    return

##微信通知
def allcontact(after_list):
    ##先获得信息体，然后进行发送
    smtp=wechat_robot.my_smtp()
    smtp.init("qq邮箱发送服务")
    message,ret=wechat_robot.my_smtp.build_message(after_list)    
    ret=smtp.send_mail(message)    
    return ret