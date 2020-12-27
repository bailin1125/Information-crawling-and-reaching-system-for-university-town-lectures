from bs4 import BeautifulSoup
import requests
import sys
import re
import os
import httplib2
sys.path.append(r"H:\my_code\some_programs\Poster_and_contact")
import Web_crawler
import My_logger
import util
import wechat_robot


##讲座信息的抽象类
class seminar:
    def __init__(self,name):
        self.name=name; ##这个讲座的名称，标题
        self.info=""; ##讲座的概要信息
        self.content=[]; ##讲座的完整内容
        self.time=""; ##讲座发布时间
        self.real_time=""; ##讲座真正开始的时间
        self.jpeg=[]; ##讲座的相关图片保存的url
        self.jpeg_real_path=[] ##讲座的真实的图片的本地地址
        self.url=""; ##针对这个讲座的url地址
        
        
        self.valid=False; ##这个讲座是否有效，是否进行推送
        self.tofile=True;##是否落到本地的逻辑，同时是否落到数据库里，一般为True
        self.type=""; ##这个讲座的类别，是属于hit还是，北大这种
        
        ##不落库的相关逻辑
        self.this_new=False ##这次是不是新的，决定这次运行要不要组装成邮件
        self.right=True  ##这个爬取的讲座是不是有什么异常

    ##建立文件夹
    @classmethod
    def mkdirs(self,path):        
        if os.path.exists(path) is False:
            try:
                os.makedirs(path)     
                #My_logger.my_logger.info("成功建立文件夹{}!".format(path))
            except:
                My_logger.my_logger.error(r"无法建立文件夹{}!".format(path))
        else:
            pass
            #My_logger.my_logger.warning(r"文件夹已经存在了！！{}!".format(path))
        return
    ##判断讲座信息是否有效
    @classmethod
    def judge_valid(seminar,singel):
        for valid_str in util.Seminar_valid_list:
                ##首先检查标题和信息
                if(valid_str in singel.info  or valid_str in singel.name):
                    print("有效数据是{},在{}出现！".format(valid_str,singel.info))
                    print("有效数据是{},在{}出现！".format(valid_str,singel.name))
                    singel.valid=True
                    return True
                ##然后是检查具体内容
                for line in singel.content:
                    if(valid_str in line):
                        print("有效数据是{},在{}出现！".format(valid_str,line))                   
                        singel.valid=True
                        return True
        return False

    ##持久化到本地文件
    def content2file(self,path):
        #print("{} in {}".format(self.content,path))
        if(self.tofile==False or self.right==False):
            return
        if os.path.exists(path)==False:
            try:
                os.makedirs(path) 
            except:
                My_logger.my_logger.error(r"无法建立文件夹{}!".format(path)) 
        ##首先把自己的标题给清洗干净
        clear_name=util.replace_valid_str(self.name)
        if(len(self.content)!=0):                
            try:               
                out_name=os.path.join(path, clear_name)
                with open(out_name+".txt","w",encoding='utf-8') as fout:
                    for line in self.content:
                        fout.write(str(line))
                        fout.write("\n")
            except Exception as e:
                My_logger.my_logger.error(r"无法向文件：{}中写入相关文件!".format(out_name))   
                My_logger.my_logger.error(r"写入文件遇到问题{}!".format(e))
        return
    
    
    
    ##微信提醒某人！！！！！！待完成
    def wechat2people(self):
        smtp=wechat_robot.my_smtp()
        smtp.init("qq邮箱发送服务")
        smtp.send_mail()
        return None
    
    ##落库
    def innersave(self):
        return None

##针对讲座信息，爬取讲座的基础方法
def get_html(url,name):
    header={'User-Agent':util.User_Agent,'Referer':util.Referer[name],"Host":util.Host[name]}
    return Web_crawler.get_html_withheader(url, header)


##这个的问题是chunked包错误，需要解决
##爬取大学城讲座单个网页信息
def get_utszlecture_one_html_old(url,title,info,path,pic_id):    
    httplib2.http.client.HTTPConnection._http_vsn = 10
    httplib2.http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0' 
    httplib2.Response.version=10
    header={'User-Agent':util.User_Agent,"Host":util.Host["utsz_lecture"],'Referer':util.Referer["utsz_lecture"]}
    ##h=httplib2.Http(timeout=5)
    real_content=requests.get(url,headers=header,timeout=120)
    for i in range(10):
        print("第{}次尝试".format(i+1))
        try:
            real_content=requests.get(url,headers=header,timeout=5)            
            break
        except:
            continue
    soup=BeautifulSoup(real_content,"html.parser")
    ##建立讲座信
    temp_obj=seminar(title) 
    temp_obj.url=url
    temp_obj.type="utsz"
    words_list=[]
    img_content=soup.find("div",{"class":"edittext"})   
    if(img_content is not None):
        for url_small in img_content.find_all("img",{"src":re.compile("jpg|png")}):
            out_name=path+"/"+title+"pic_"+str(pic_id)+".jpg" 
            
            Web_crawler.get_jpeg_out(url_small["src"], out_name)   
            temp_obj.jpeg_real_path.append(out_name)
            #print("已写入：{}张图片".format(pic_id+1))           
            pic_id+=1
            temp_obj.jpeg.append(url_small["src"])      
    
    #然后是讲座内容
    words_content= soup.find("div",{"class":"edittext"})    
    if(words_content is not None):
        for item in words_content.find_all("p"):
            if(util.judge_str(item.string)==True):                
                words_list.append(item.string)
        temp_obj.content=words_list 
    My_logger.my_logger.warning("已完成爬取：{}".format(title))
    return temp_obj


##爬取大学城讲座单个网页信息
##虽然有了信息，但是这里我们使用详细版的信息
def get_utszlecture_one_html(url,title,real_time,path,pic_id): 
    header={'User-Agent':util.User_Agent,"Host":util.Host["utsz_lecture"],'Referer':util.Referer["utsz_lecture"]}
    ##h=httplib2.Http(timeout=5)
    real_content=requests.get(url,headers=header,timeout=120).text
    soup=BeautifulSoup(real_content,"html.parser")
    
    ##建立讲座信息
    temp_obj=seminar(title) 
    temp_obj.url=url
    temp_obj.real_time=real_time
    temp_obj.type="utsz"
    words_list=[]
    seminar.mkdirs(path)
    ##开始爬取相关内容
    try:
        main_part=soup.find("div",{"class":"conboxcon reset-conboxcon"}).find_all("p")
    except Exception as e:
        My_logger.my_logger.error("{}：不符合爬取预期，跳过,错误{}！".format(url,e))
        ress=seminar("-100")
        ress.right=False
        return ress     
    for ele in main_part:
        jpeg_list=ele.find_all("img")
        try:
            if(len(jpeg_list)==0):
                ##说明是文字
                if(util.judge_str(ele.get_text())==True):
                    words_list.append(ele.get_text())
            else:
                for singel in jpeg_list:
                    ura=singel.get("src")                    
                    out_name=path+"/"+"pic_"+str(pic_id)+".jpg"
                    Web_crawler.get_jpeg_out(ura, out_name)
                    temp_obj.jpeg_real_path.append(out_name)
                    #print("已写入：{}张图片".format(pic_id+1))          
                    pic_id+=1           
        except Exception as e:
            My_logger.my_logger.error("发现问题{}!".format(e))
            My_logger.my_logger.error("爬取大学城的{}讲座时候遇到问题！".format(title))
    temp_obj.content=words_list   
    My_logger.my_logger.warning("已完成爬取：{}".format(title))
    return temp_obj


##获取大学城讲座的列表信息
##已经可以返回题目，真实时间以及信息
def get_utszlecture_SEMINAR(org_url):
    content=BeautifulSoup(get_html(org_url,"utsz_lecture"),"html.parser")
    yugao=content.find("ul",{"class":"part_body_list reset-margin"})
    #print(yugao)    
    url_list=[]
    title_simple_list=[]
    info_list=[]
    real_time_list=[]

    for article in yugao.find_all("li"):
        url,titel,real_time,info=UTSZ_help_seminar(article)        
        url_list.append(url)
        title_simple_list.append(titel)
        info_list.append(info)
        real_time_list.append(real_time)            
    # print(title_simple_list)
    # print(url_list)
    # print(info_list)   
    My_logger.my_logger.info("扫描大学城图书馆信息完毕，需要爬取{}场讲座信息".format(len(title_simple_list)))
    return url_list,title_simple_list,info_list,real_time_list

##帮助从一个元素中获取对应的信息
def UTSZ_help_seminar(li):
    org_url="https://lib.utsz.edu.cn"
    titel=""
    url=""
    real_time=""
    info=""    
    url=org_url+li.find_all("a")[1].get("href")
    titel=li.find_all("a")[1].get_text()    
    real_time=li.find("span",class_="time_field").get_text().split("：",1)[1]
    info=li.find("span",class_="site_field").get_text()
    return url,titel,real_time,info
    
    


##爬取哈工大的一条讲座信息
def get_HIT_one_html(url,title,real_time,time,path,pic_id):
    header={'User-Agent':util.User_Agent,'Referer':util.Referer["HIT"],"Host":util.Host["HIT"]}
    content=Web_crawler.get_html_withheader(url, header)
    soup=BeautifulSoup(content,"html.parser")
    ##先爬取一个标题
    words_list=[] 
    org_jpeg_url="http://www.hitsz.edu.cn"
    ##构建讲座类存储信息
    try:
        temp_obj=seminar(title)  
        temp_obj.time=time
        temp_obj.real_time=real_time
        temp_obj.url=url
        temp_obj.type="HIT"
        seminar.mkdirs(path)
    #然后是讲座信息等相关  
        main_part=soup.find("div",class_="detail")
    except Exception as e:
        My_logger.my_logger.error("{}：不符合爬取预期，跳过,错误{}！".format(url,e))
        ress=seminar("-100")
        ress.right=False
        return ress 
    for ele in main_part.find_all("p"):
        jpeg_list=ele.find_all("img")
        # print(ele.get_text())
        # print(len(jpeg_list)==0)
        try:
            if(len(jpeg_list)==0):
                ##说明是文字
                if(util.judge_str(ele.get_text())==True):
                    words_list.append(ele.get_text())
            else:
                for singel in jpeg_list:
                    ura=org_jpeg_url+singel.get("src")                    
                    out_name=path+"/"+"pic_"+str(pic_id)+".jpg"
                    Web_crawler.get_jpeg_out(ura, out_name)
                    temp_obj.jpeg_real_path.append(out_name)
                    #print("已写入：{}张图片".format(pic_id+1))          
                    pic_id+=1           
        except Exception as e:
            My_logger.my_logger.error("发现问题{}!".format(e))
            My_logger.my_logger.error("爬取哈工大的{}讲座时候遇到问题！".format(title))
    temp_obj.content=words_list    
    My_logger.my_logger.info("已完成爬取{}!".format(title))
    return temp_obj



##获得哈工大的讲座列表
##可以返回标题，真实时间和发布时间
def get_HIT_SEMINAR(org_url):
    content=BeautifulSoup(get_html(org_url,"HIT"),"html.parser")
    yugao=content.find("ul",{"class":"lecture_n"})
   
    url_list=[]
    title_simple_list=[]
    time_list=[]
    real_time_list=[]   

    
    for article in yugao.find_all("li"): 
        url,titl,real_time,time=HIT_help_semiahnr(article)        
        url_list.append(url)
        title_simple_list.append(titl)
        real_time_list.append(real_time)
        time_list.append(time)         
    #print(title_simple_list)
    #print(url_list)
    #print(info_list)
    #print(info_list)  
    My_logger.my_logger.info("扫描哈工大信息完毕，需要爬取{}讲座信息".format(len(title_simple_list)))
    return url_list,title_simple_list,real_time_list,time_list


##辅助性质的从hit的一条element中获取相关信息
def HIT_help_semiahnr(li):
    hit_org="http://www.hitsz.edu.cn"
    titl=""
    real_time=""
    time=""##发布时间
    url=""
    
    url=hit_org+li.find("a").get("href")
    titl=li.find("a").get_text()
    time=li.find("span",class_="date_t").get_text()
    ##注意真实时间的返回方法，采用组合的样子
    temp_list=[]
    temp_list=li.find("span",class_="date").get_text().split()   
    for con in temp_list:
        real_time+=con
    return url,titl,real_time,time


##获得清华的一条讲座
def get_TSINGHUA_one_html(url,time,path,pic_id):
    content=get_html(url,"TSINGHUA")
    soup=BeautifulSoup(content,"html.parser")    
    ##先爬取一个标题
    try:
        title=soup.find("h1",{"class":"arti_title"})
        temp_obj=seminar(title.string)  
        temp_obj.url=url
        temp_obj.type="TSINGHUA"
        temp_obj.time=time
        content=[] ##讲座的内容
    #然后是讲座信息等相关  
    ##预防会产生图片和文字的所有可能
        org_jpeg_url="https://www.sigs.tsinghua.edu.cn"
        main_part=soup.find("div",class_="wp_articlecontent").find_all("p")
        seminar.mkdirs(path)
    except Exception as e:
        My_logger.my_logger.error("{}：不符合爬取预期，跳过,错误{}！".format(url,e))
        ress=seminar("-100")
        ress.right=False
        return ress 
    for ele in main_part:
        jpeg_list=ele.find_all("img")
        try:
            if(len(jpeg_list)==0):
                ##说明这是文字
                if(util.judge_str(ele.get_text())==True):
                    content.append(ele.get_text())
            else:
                for singel in jpeg_list:
                    ura=org_jpeg_url+singel.get("src")
                    temp_obj.jpeg.append(org_jpeg_url+ura)                    
                    out_name=path+"/"+"pic_"+str(pic_id)+".jpg"
                    Web_crawler.get_jpeg_out(ura, out_name)
                    temp_obj.jpeg_real_path.append(out_name)
                    #print("已写入：{}张图片".format(pic_id+1))         
                    pic_id+=1         
        except Exception as e:
            My_logger.my_logger.error("发现问题{}!".format(e))
            My_logger.my_logger.error("爬取清华的{}讲座时候遇到问题！".format(title.string))
   
    temp_obj.content=content
    My_logger.my_logger.warning("已完成爬取：{}".format(title.string))
    return temp_obj



##获取清华的讲座列表
##只提供了发布时间和题目
def get_TSINGHUA_SEMINAR(org_url):
    ##content=BeautifulSoup(get_html(org_url,"TSINGHUA"),"html.parser")
    ##这里我们使用selenium来获取相关信息
    header={'User-Agent':util.User_Agent,'Referer':util.Referer["TSINGHUA"],"Host":util.Host["TSINGHUA"]}
    ##初始化一个selenimu的东西
    chrome=Web_crawler.web_selenium("chrome")
    content=BeautifulSoup(chrome.get_source(org_url),"html.parser")
    try:
        yugao=content.find("div",{"class":"contain_news xwlist"})
        #print(yugao)
    except Exception as e:
        My_logger.my_logger.error("{}：不符合爬取预期，跳过,错误{}！".format(org_url,e))
        return [],[],[]
    
    url_list=[]
    title_simple_list=[]
    time_list=[]

    for article in yugao.find_all("div",{"class":"mox_list"}):         
        title_simple_list.append(article.find("div",{"class":"news_title"}).get_text())
        time_list.append(article.find("div",{"class":"news_time"}).get_text())
        url_list.append(article.find("a")["href"])
        
              
    #print(title_simple_list)
    #print(url_list)
    #print(info_list)  
    My_logger.my_logger.info("扫描清华信息完毕，需要爬取{}讲座信息".format(len(title_simple_list)))
    return url_list,title_simple_list,time_list



##获取国法的一条讲座
def get_STL_one_html(url,info,path,pic_id):    
    content=get_html(url,"STL")
    soup=BeautifulSoup(content,"html.parser")
    
    main_part=soup.find("div",class_="cell large-auto")
    title=main_part.find("h1").get_text()
    temp_obj=seminar(main_part.find("h1").get_text())  
    if(len(info)>=40):
        temp_obj.real_time=info[:39]
    else:
        temp_obj.real_time=info
    temp_obj.url=url
    temp_obj.type="STL"
    #然后是讲座信息等相关
    content=[]
    seminar.mkdirs(path)
    ##首先是文字部分
    for ele in main_part.find_all("p"):
        try:                 
            if(util.judge_str(ele.get_text())==True):
                content.append(ele.get_text())   
        except Exception as e:
            My_logger.my_logger.error("发现问题{}!".format(e))
            My_logger.my_logger.error("爬取国法讲座：{}中遇到问题，重试！".format(main_part.find("h1").get_text()))
    temp_obj.content=content
    ##然后是图片部分
    for ele in main_part.find_all("figure"):
         ura=ele.find("img").get("src")
         temp_obj.jpeg.append(ura)         
         out_name=path+"/"+"pic_"+str(pic_id)+".jpg"
         Web_crawler.get_jpeg_out(ura, out_name)       
         temp_obj.jpeg_real_path.append(out_name)
         #print("已写入：{}张图片".format(pic_id+1))         
         pic_id+=1         
    My_logger.my_logger.warning("已完成爬取：{}".format(title))
    return temp_obj



##获取国法的讲座列表
def get_STL_SEMINAR(org_url):  ##返回每个讲座的url，小标题以及时间地点信息
    content=BeautifulSoup(get_html(org_url,"STL"),"html.parser")   
    key_words=["活动","讲座","分享","预告"]

    info_list=[] ##注意这里现在没有info只有time了
    ##并且注意这里已经返回了真实的时间了
    url_list=[]
    title_simple_list=[]


    for article in content.find("div",class_="cell large-auto").find_all("div",class_="cell auto item-content"): 
        try:
            ele=article            
            title_simple_list.append(ele.find("a").get_text())
            url_list.append(ele.find("a").get("href"))        
            info_list.append(ele.find("p").get_text()) 
        except Exception as e:
            My_logger.my_logger.error("获取国法的讲座列表中途出错，跳过{}！".format(e))
            continue
    #print(title_simple_list)
    #print(url_list)
    #print(info_list)  
    My_logger.my_logger.info("扫描国法信息完毕，需要爬取{}讲座信息".format(len(title_simple_list)))
    return url_list,title_simple_list,info_list





##获取汇丰的讲座列表
def get_HSBC_SEMINAR(org_url):
    content=BeautifulSoup(get_html(org_url,"HSBC"),"html.parser")
    yugao=content.find("div",class_="little-main-list txt-list").find_all("li")     
    time_list=[]
    url_list=[]
    title_simple_list=[]
    
    ##重新修改获取元素的统计
    ##注意这里返回的是发布时间，不是真实时间
    ##汇丰网页只有图片有真实的讲座时间
    for ele in yugao: 
        time_list.append(ele.find("span").get_text())
        url_list.append(ele.find("a").get("href")) 
        title_simple_list.append(ele.find("h2").get_text())
        
    My_logger.my_logger.info("扫描汇丰信息完毕，需要爬取{}讲座信息".format(len(time_list)))
    return time_list,url_list,title_simple_list
    



##获取汇丰的一条信息
def get_HSBC_onehtml(url,time,path,pic_id):    ##需要的url，生成的路径，产生的内容文件名字，图片的递增序列
     content=get_html(url,"HSBC")
     soup=BeautifulSoup(content,"html.parser")     
     ##
     try:
         main_part=soup.find("div",class_="common")
         title=main_part.find("div",class_="title").get_text()
         ##构建讲座信息
         temp_obj=seminar(title)
         temp_obj.time=time
         temp_obj.url=url
         temp_obj.type="HSBC"
         #然后是讲座信息等相关
         content=[]
         ##不同的讲座内容对应不同的网页信息展示   
         main_part=main_part.find("div",class_="content clearfix")
         seminar.mkdirs(path)
         main_list=[]
         main_list=main_part.find_all("div")
     except Exception as e:
         My_logger.my_logger.error("{}：不符合爬取预期，跳过,错误{}！".format(url,e))
         ress=seminar("-100")
         ress.right=False
         return ress 
    
     for ele in main_list:
          try:
              jpeg_list=ele.find_all("img")
              if(len(jpeg_list)==0):
                  ##说明是文本文键
                  if(util.judge_str(ele.get_text())==True):
                      content.append(ele.get_text())
              else:
                  for singel in jpeg_list:
                      ura=singel.get("src")
                      temp_obj.jpeg.append(ura)                     
                      out_name=path+"/"+"pic_"+str(pic_id)+".jpg"
                      if("img-user"in ura):
                          continue
                      Web_crawler.get_jpeg_out(ura, out_name)
                      temp_obj.jpeg_real_path.append(out_name)
                      #print("已写入：{}张图片".format(pic_id+1))              
                      pic_id+=1
          except Exception as e:
              My_logger.my_logger.error("发现问题{}!".format(e))
              My_logger.my_logger.error("爬取汇丰{}讲座时遇到问题，重试！".format(title))
     temp_obj.content=content
     My_logger.my_logger.warning("已完成爬取：{}".format(title))
     return temp_obj
