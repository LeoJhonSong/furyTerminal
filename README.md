# furyTerminal文档

目录

---
1. [简介](#简介)
   1. [文档目的](#文档目的)
   2. [发起时间](#发起时间)
   3. [规划](#规划)
      1. [TODO](#TODO)
      2. [FIXME](#FIXME)
      3. [Milestone](#Milestone)
   4. [系统目标](#系统目标)
   5. [系统环境](#系统环境)
2. [CAN转SPI模块](#CAN转SPI模块)
3. [DSI接口的7寸触摸显示屏](#DSI接口的7寸触摸显示屏)
4. [测试](#测试)
5. [树莓派配置](#树莓派配置)
   1. [网络配置](#网络配置)
   2. [开启热点](#开启热点)
6. [车载网站 (交互平台)](#车载网站-交互平台)
   1. [站点地图](#站点地图)
   2. [如此选择的优缺点](#如此选择的优缺点)
      1. [Django](#Django)
         1. [优点](#优点)
         2. [缺点](#缺点)
      2. [MySQL](#MySQL)
         1. [MySQL命令简记](#MySQL命令简记)
   3. [管理](#管理)
   4. [oncar](#oncar)
      1. [oncar设计](#oncar设计)
   5. [django纪要](#django纪要)
      1. [设置允许访问的地址](#设置允许访问的地址)
      2. [设置后台时间显示格式](#设置后台时间显示格式)
      3. [设置字段不可修改](#设置字段不可修改)
      4. [模板](#模板)
      5. [常用命令](#常用命令)
         1. [运行网站](#运行网站)
         2. [生成应用的迁移](#生成应用的迁移)
         3. [应用迁移到网站](#应用迁移到网站)
         4. [database API](#database-API)
            1. [进入专用python解释器](#进入专用python解释器)
            2. [添加记录](#添加记录)
      6. [注意事项](#注意事项)
   6. [页面设计纪要](#页面设计纪要)
      1. [仪表盘](#仪表盘)
---

## 简介

### 文档目的

本文档是furyTerminal系统总体和各部分说明, 主要面向电气组开发人员, 其他组成员不应需要阅读
本文档, 系统实现的应当是十分友好 (傻瓜式) 的交互😁

### 发起时间

2019-02-01

### 规划

#### TODO

- oncar tab页 (车手页, 设备页, 关机)
- 传感器调试, 安全回路状态界面
  - 油门深度 (单色直柱)
  - 刹车深度 (单色直柱)
  - 安全电路状态图
- 车手界面mcMessage alert报警
- 开机图片/动画. 可参考 🔗[YouTube上一个人给树莓派换Spalsh Screen](https://www.youtube.com/watch?v=VK_eBe53Stc)
- 电池箱温度热力图

#### FIXME

- 将开机启动网页的时间提前
- mysql数据库延迟 (应该是和事务独立等级有关)

#### Milestone

- 为每个车手建立账号分别记录数据
- 将每次跑动的时间, 速率, 方向, 油门, 刹车, 电量等关联起来, 达到还原整次跑动的效果, 方便实时/
  后期的分析
- 语音提示

### 系统目标

命名为furyTerminal是因为本系统的目标是做出一个 **友好, 直观, 健壮** 的赛车
终端:

- 让操作方式足够友好, 车队队员们能通过简单操作来获取数据或者更改参数
- 数据呈现方式, 交互方式足够直观, 速度, 油门, 时间等车手常用数据明显, 故障原因提示内容足够直观, 分析用数据以图表形式呈现
- 系统足够健壮, 能够应对绝大多数故障情况, 比如掉电数据储存等.

至于什么是终端 (Terminal), 参见 🔗 [这里](https://www.zhihu.com/question/21711307/answer/118788917)

![系统蓝图](doc/蓝图.png)

### 系统环境

`Linux` version: 4.14.34-v7+ (dc4@dc4-XPS13-9333) (gcc version 4.9.3 (crosstool-NG crosstool-ng-1.22.0-88-g8460611)) #1110 SMP Mon Apr 16 15:18:51 BST 2018

`Raspbian` version: Raspbian GNU/Linux 9.6 (stretch)

❗️ 当前使用[中科大源](https://lug.ustc.edu.cn/wiki/mirrors/help/raspbian)

`python` version: Python 3.5.3 (default, Sep 27 2018, 17:25:39) [GCC 6.3.0 20170516] on linux

💡 当前系统默认python为 3.5.3, 若想将系统默认python切换回python2, 运行以下命令然后跟随指导操作.

```shell
sudo update-alternatives --config python
```

⚠️需注意pip的版本与python版本相匹配, 通过运行 `pip -V` 来查看pip版本和位置

`django` version: 2.1.7

## CAN转SPI模块

📑 [RS485 CAN HAT用户手册](doc/CAN2SPI/CAN_to_SPI_module/RS485-CAN-HAT-user-manual-cn.pdf)

📑 [RS485 CAN HAT电路图](doc/CAN2SPI/CAN_to_SPI_module/RS485_CAN_HAT_Schematic.pdf)

🔗 [python-can文档](https://python-can.readthedocs.io/en/master/index.html#)

## DSI接口的7寸触摸显示屏

📑 [7寸触摸屏说明书](doc/display/7寸触摸屏说明书.md)

## 测试

位于`/test`文件夹下的为各部分测试程序


## 树莓派配置

### 网络配置

🔗 [设置固定IP](https://www.jianshu.com/p/308fb22a7dab)

### 开启热点

TODO

## 车载网站 (交互平台)

之所以选择做网站是因为网站是最容易实现的GUI, 也能很轻松地接入大量库, 轻松实现远程访问等功能.

只要开机自启浏览器全屏模式, 用代码避免误触露出端倪, 根本看不出是网页!🎉

❗️ 目前树莓派没有设置正常关机方式, 就是断电关机, 因此再次启动chromium时右上角会显示 "Restore pages?" 通过匿名模式开启网页避免出现这个提示.

防止误触露出端倪具体来说指**隐藏鼠标图标**, **禁用右键菜单**, **禁止选中**等

🔗 [防止误触相关代码](https://blog.csdn.net/jx950915/article/details/80346530)

本网站基于 **Django** 框架和MySQL数据库.

### 站点地图

- `/` (Home Page)
  - `/oncar`
    - `/` (车手页面)
    - `/devices` (赛前设备状态检查页)
    - `/refresh` (不是访问页面, 是给车手页面刷新数据的)
  - `/remote`

### 如此选择的优缺点

#### Django

##### 优点

- 是一个python框架, 数据处理很方便, 容易接入ROS
- 容易上手. 个人认为结合了前后端, 更偏向后端, 但前端能很容易的结合前端

##### 缺点

速度不算快

#### MySQL

一开始使用的是SQLite, 但是[SQLite不支持高并发访问](https://blog.csdn.net/u013690521/article/details/38776709),
因此改用MySQL.

##### MySQL命令简记

💡 root用户初始密码为空, 只能`su`到root用户进入mysql

命令行进入mysql `mysql -u fury -p`

新建数据库 `create database furyTerminal character set utf8;`  
删除数据库 `drop database furyTerminal;`  
查看数据库中的数据表 `use furyTerminal; show tables;`  
新建用户 `create user fury identified by 'fury';`  
给予用户权限 `grant all privileges on furyTerminal.* to fury;`  
查看用户权限 `show grants for fury;`  
查看所有用户 `select user, host from mysql.user;`

👇一些推荐的学习资料

🔗 [HTML教程](https://www.w3schools.com/html/default.asp)  
🔗 [CSS教程](https://www.w3schools.com/css/default.asp)  
🔗 [Bootstrap教程](https://www.w3schools.com/bootstrap4/default.asp)  
🔗 [Bootstrap官方文档](https://getbootstrap.com/docs/4.3/getting-started/introduction/)  
🔗 [JavaScript教程](https://www.w3schools.com/js/default.asp)  
🔗 [Django官方文档中文版](https://docs.djangoproject.com/zh-hans/2.1/) (翻译不全)  
🔗 [Django**2.2**文档个人中文翻译](http://www.liujiangblog.com/course/django/2)  
🔗 [Django MySQL数据库文档](https://docs.djangoproject.com/en/2.2/ref/databases/#time-zone-definitions)

### 管理

管理员账号: leo

密码: leo

💡 添加管理员 `python manage.py createsuperuser`

### oncar

#### oncar设计

📝 [oncar面板设计草稿](doc/furyTerminal/oncar/面板设计草稿.md)

### django纪要

#### 设置允许访问的地址

在 `furyTerminal/furyTerminal/settings.py` 中 **ALLOWED_HOSTS**一项设置了允许访问
网站的地址, 设为 `'*'` 则是允许所有地址访问.

#### 设置后台时间显示格式

🔗 [可用的格式化字符](https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date)
🔗 具体参考[这里](https://blog.51cto.com/xujpxm/2090382)

#### 设置字段不可修改

在对应的父类为 **admin.ModelAdmin** 的类下重写 `get_readonly_fields`方法如下:

```python
def get_readonly_fields(self, request, obj=None):
    if obj:  # obj is not None, so this is an edit
        return ['[readonly_fields]']  # Return a list or tuple of readonly fields' names
    else:  # This is an addition
        return []
```

#### 模板

🔗 参考链接:
- [模板的导入和继承, 静态文件的使用](https://blog.csdn.net/qq_33961117/article/details/83993039)
- [Django2.2文档翻译-模板层](http://www.liujiangblog.com/course/django/145)

🔗 [参考](https://stackoverflow.com/questions/7860612/django-admin-make-field-editable-in-add-but-not-edit)

#### 常用命令

💡 因为我记性很差, 将常用命令集成到了根目录下的python脚本`fury`

##### 运行网站

⚠️ 在网站根目录执行.
💡此时为网站在 **localhost:8000** 运行

```shell
python furyTerminal/manage.py runserver 0:8000
```

##### 生成应用的迁移

```shell
python manage.py makemigrations
```

##### 应用迁移到网站

⚠️ 在网站根目录执行.

```shell
python manage.py migrate
```

##### database API

###### 进入专用python解释器

> 我们使用这个命令而不是简单的使用 "Python" 是因为 **manage.py** 会设置
> **DJANGO_SETTINGS_MODULE** 环境变量，这个变量会让 Django 根据 **mysite/settings.py**
> 文件来设置 Python 包的导入路径。

```shell
python manage.py shell
```

💡如果想通过脚本调用 database API, 需要在脚本开头加上以下语句:

```python
from furyTerminal import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furyTerminal.settings')
django.setup()
```

具体例子参见[oncar应用的Speed部分的测试](test/oncar/speed-gauge/create.py)

###### 添加记录

举例: 向 **oncar** 应用的 **Speed** 模型添加记录

1.首先当然是引用它

```python
from oncar.models import Speed
```

2.有两种添加方法:

   1. 先实例化然后保存 🔗[save()](https://docs.djangoproject.com/zh-hans/2.1/topics/db/queries/)

      ```python
      speeed = Speed(speed_value='123')
      speeed.save()
      ```

   2. 直接创建 🔗[creat()](https://docs.djangoproject.com/zh-hans/2.1/ref/models/querysets/#django.db.models.query.QuerySet.create)

      ```python
      Speed.objects.create(speed_value='123')
      ```

#### 注意事项

- path()函数的参数`route`不会匹配 GET 和 POST 参数或域名。例如，URLconf 在处理请求
  https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ 。处理请求
  https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/。
- 🔗[django模型中auto_now和auto_now_add的区别](https://www.cnblogs.com/vincenshen/articles/7659763.html)

### 页面设计纪要

#### 仪表盘

最开始自己手搓的仪表盘显得有些卡顿, 能达到0.5秒级刷新, 再快很容易让chrome崩溃. 这个刷新率听起来不低, 0.5s的延迟在汽车上不算高, 但呈现出来的**变化过程不够平滑**, 给人一种卡顿感.

🔗 [这个](https://www.codewall.co.uk/creating-gauge-charts-with-the-justgage-javascript-library/)是一个最简陋的有平滑移动的仪表盘的教程

🔗 [这个](https://www.pubnub.com/blog/streaming-sensor-readings-realtime-gauge-chart/)是一个用树莓派读取传感器参数并显示在网页仪表盘的实例

🔗 [这个](https://developers.google.com/chart/interactive/docs/gallery/gauge)是Google Charts的**朴素派**仪表 (效果如下图)

![1570749713523](doc/google_gauge.png)

🔗 [这个](https://www.cssscript.com/canvas-based-html5-gauge-library-gauge-js/)是目前找到最符合赛车样式的仪表 (好吧梁师傅说没有科技感), 由**canvas**绘制. 刷新值代码:

```js
document.gauges[0].value = current_speed;
```

![](doc/old-fashion-gauge.gif)

![](doc/black-red-old-fashion-gauge.jpg)

🔗 [这个](https://www.cssscript.com/animated-svg-gauge/)是科技简约风的, 由**svg**绘制, 刷新值代码:

```js
speedGauge.setValue(10)
```

![](doc/svg-modern-gauge.gif)