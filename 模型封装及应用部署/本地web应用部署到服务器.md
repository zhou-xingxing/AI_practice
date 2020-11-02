

# 本地web项目部署到服务器

(前置步骤：安装宝塔及apache/nginx，完成本地web应用)

---

## 整体流程：

1. 打开本地应用，在pycharm的terminal中```pip freeze >requirements.txt ``` 导出所有的第三方包

2. 上传项目到服务器

3. 安装python3

4. 安装virtualenv

5. 在该项目下启动虚拟环境

6. ```pip install -r requirements.txt``` 在该虚拟环境下安装所有程序的依赖模块

7. ```python manage.py``` 运行程序，查看IP及端口号

8. 宝塔界面：网站->添加站点(域名填服务器的公网地址)

9. 设置->配置文件

   apache 在文件中加上

   ```
   ProxyPass / http://127.0.0.1:5000/
   ProxyPassReverse /  http://127.0.0.1:5000/
   ```

   nginx 在文件中加上

   ```
   location / {
     	proxy_pass http://127.0.0.1:5000;
   }
   ```

10. 运行程序：```cd 项目根目录```，```# source venv/bin/activate ``` 启动虚拟环境，```python manage.py``` 运行程序

## python3安装

---

1. 安装python3之前，可能需要安装以下依赖包

```shell
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install -y libffi-devel zlib1g-dev
yum install zlib* -y
```

1. ```# mkdir /usr/local/python3``` 在/usr/local/目录下建立python3文件夹

2. ```# cd /usr/local/python3``` 打开这个文件夹

3. ```# wget http://mirrors.sohu.com/python/3.7.4/Python-3.7.4.tgz``` 下载安装包

4. ```# tar -xvzf Python-3.7.4.tgz``` 解压

5. ```# cd Python-3.7.4``` 进入Python-3.7.4文件夹

6. ```# ./configure --prefix=/usr/local/python3``` 配置安装路径

7. ```# make && make install ``` 编译、安装可执行文件

8. ```# ln -s /usr/local/python3/bin/python3 /usr/bin/python3```

	```# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3```

	使用命令创建软连接

9. ```python3 -V```

	若显示版本等信息就为安装成功

## virtualenv安装及使用

---

若没有虚拟环境，所有第三方的包都会被pip安装在python的site-packages目录下,但有的时候不太应用的依赖包会需要不同版本的，virtualenv就是解决这个问题的，它可以建立一套独立的Python运行环境。

1. 进根目录，```# pip install virtualenv```

2. ```# cd 项目的根目录```

	```# virtualenv -p /usr/bin/python3 venv``` 新建一个python3的虚拟环境（/usr/bin/python3是刚刚安装的python3的路径；venv是虚拟环境的名字，可修改）

3. ```# source venv/bin/activate ``` 启动虚拟环境，启动后就可以看到命令提示符前有个(venv)