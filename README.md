# tgchat的服务器端
## 部署方法
### 开启socket服务器端
  * cd /ChatTogether
  * python3 Chatsocket.py
### 部署django:
  #### 迁移数据库: 
  * python3 manage.py makemigration
  * python3 manage.py migrate
  ####  开启django: 
  * python3 manage.py runserver 0:8888
## 持久化运行方法
使用nohup命令;
    
