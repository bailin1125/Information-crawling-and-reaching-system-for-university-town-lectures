# Information-crawling-and-reaching-system-for-university-town-lectures
  通过requests和selenium爬取大学城5个网站的所有讲座信息，并通过触达模块（邮箱，微信机器人，qq，短信）等触达给指定用户  
## 项目来源：  
  本来是之前研一写过的一个小需求，最近女票根据这个提了新的想法（产品经理），然后利用课余时间将之前的代码完全重构。并利用在阿里实习认识到的一些思想和技术加以完善。做到了代码通俗易懂，鲁棒性好，异常处理完善等要求。    
  本来是一个练手小项目，但是感觉这个过程也是加深了对于python的认识，再次认识到编程不应掣肘于语言。斗胆发出来，一起学习交流！  
## 技术特点：  
  1：后台数据库与业务模块分离。（数据库：sql 2019）  
  2：可靠的异常处理和全局单例的日志记录模块。  
  3：可靠的网页爬取模块和html分析模块，支持对于ajax异步加载的网页爬取问题。  
  4：多样的触达模块可选（微信，qq，短息，邮件）。  
  5：基于面向对象，迭代周期减少。  
  6：基础设计模式的使用以及尽量追求代码风格的简洁易懂，模块依赖关系清晰。  
## 使用方法:    
1：git clone该项目  
2: 看readme.txt了解config.ini的设置，并完成设置（最好再看看模块关系图加深理解）。  
3：基于个人需求，修改util相关全局常量以及数据库连接的常量。  
4：运行main.py  
5：等待结束。  
