# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:17:28 2020
封装的相关日志操作
@author: 王志
"""

import logging



##logging模块的初始化操作
##返回初始化模块的logger
##幸运的是，logging是单例模式且全局线程安全
my_logger=None
def init():
#先定义日志操作
    logger=logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    handler1=logging.StreamHandler()
    handler2=logging.FileHandler(filename="logging_user",encoding='utf-8')
    handler1.setLevel(logging.DEBUG)
    handler2.setLevel(logging.ERROR)
    formatter=logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    #定义处理器，用于文件输出和控制台输出
    while(len(logger.handlers)>2):
        logger.handlers.pop()
    global my_logger
    my_logger=logger    
    return logger


