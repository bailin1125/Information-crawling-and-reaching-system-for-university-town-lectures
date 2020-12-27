# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 14:16:01 2020
方法进行的主函数
@author: 王志
"""

#版权相关信息
copy_right='''All rights reserved from bailin 2019.9.8 from PKU@SAM
update data:2020.12.24
version number :2.0'''
import util
import My_logger
from Seminar import get_seminar

def main():
    print("{0:-^30}".format(copy_right))
    print("-----------------------------------------------------")
    print("\n")
   
    #初始化配置文件读取和日志
    My_logger.init()    
    util.init()
    
    
    
    ##开始寻找讲座
    My_logger.my_logger.info("开始按照配置文件搜寻讲座信息！")
    all_obj=get_seminar.find_seminaer()
    My_logger.my_logger.info("搜寻讲座信息完成，共发现:{}场讲座！".format(len(all_obj)))
    
    ##讲座分辨
    get_seminar.judge_seminar(all_obj)
    My_logger.my_logger.info("讲座主题分辨完成！")
    
    ##讲座的落库
    get_seminar.alltoDB(all_obj)
    My_logger.my_logger.info("讲座落库完成！")
    
    # ##讲座持久化到本地
    get_seminar.toreal_file(all_obj)
    My_logger.my_logger.info("讲座持久化完成！")
    
    ##讲座的微信通知   
    get_seminar.allcontact(all_obj)
    My_logger.my_logger.info("讲座信息邮件推送完成！")
    
    
    
    
    
   

if __name__=="__main__":
    main()
    print("all total work done!")
