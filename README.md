# APKVersionManage

# 介绍
 对Android APK版本进行管理，下载。
 

# 软件架构
Centos7.4 + Python3 + Flask + mysql + nginx + uwsgi

# 安装教程


一、数据库配制：

需要在Centos7.4系统版本上安装mysql， 并设置mysql的数据库名称为：APPPlatform
设置mysql的用户名与密码，设置好后将config.py中USERNAME， PASSWORD的字段修改成配置好的用户名与密码（默认端口3306）
二、Flask可执行的虚拟环境搭建：

将代码拷贝到虚拟环境的目录
执行以下命令： 
''' python manage.py db init 
    python manage.py db migrate
    python manage.py db upgrade 
'''
以上数据库表就完成了创建
          
三、安装uwsgi并修改uwsgi.ini文件

四、安装ngnix并修改nginx.conf文件

以上安装教程可以参考：https://blog.csdn.net/Jayden_Gu/article/details/103031930

# 修改config.py文件
'''
# config databases
HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'PinnetRelease'
PORT = '3306' 

# config Email
MAIL_SERVER = 'XXXXXXX'
MAIL_PORT = 25
MAIL_USERNAME = 'XXXXXXXX'
MAIL_PASSWORD = "XXXXXXX"  # 邮箱授权码，不是邮箱密码
MAIL_DEFAULT_SENDER = 'XXXXXXXX'

'''
