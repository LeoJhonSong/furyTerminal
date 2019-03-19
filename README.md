# furyTerminal文档

1. [简介](#简介)
   1. [文档目的](#文档目的)
   2. [发起时间](#发起时间)
   3. [系统目标](#系统目标)
   4. [系统环境](#系统环境)
2. [oncar](#oncar)
   1. [oncar设计方针](#oncar设计方针)
3. [django纪要](#django纪要)
   1. [设置允许访问的地址](#设置允许访问的地址)
   2. [常用命令](#常用命令)
      1. [运行网站](#运行网站)
      2. [生成应用的迁移](#生成应用的迁移)
      3. [应用迁移到网站](#应用迁移到网站)
   3. [注意事项](#注意事项)

## 简介

### 文档目的

本文档是furyConsole系统总体和各部分说明, 主要面向电气组开发人员, 其他组成员不应需要阅读
本文档, 系统实现的应当是十分友好 (傻瓜式) 的交互😁

### 发起时间

2019-02-01

### 系统目标

命名为furyTerminal是因为本系统的目标是做出一个**友好, 直观, 健壮**的赛车
终端:

- 让操作方式足够友好, 车队队员们能通过简单操作来获取数据或者更改参数
- 数据呈现方式, 交互方式足够直观, 速度, 油门, 时间等车手常用数据明显, 故障原因提示内容
  足够直观, 分析用数据以图表形式呈现
- 系统足够健壮, 能够应对绝大多数故障情况, 比如掉电数据储存等.

![系统蓝图](doc/蓝图.png)

至于什么是终端 (Terminal), 参见 🔗 [这里](https://www.zhihu.com/question/21711307/answer/118788917)

### 系统环境

`Linux` version: 4.14.34-v7+ (dc4@dc4-XPS13-9333) (gcc version 4.9.3 (crosstool-NG crosstool-ng-1.22.0-88-g8460611)) #1110 SMP Mon Apr 16 15:18:51 BST 2018

`Raspbian` version: Raspbian GNU/Linux 9.6 (stretch)

❗️ 当前使用[中科大源](https://lug.ustc.edu.cn/wiki/mirrors/help/raspbian)

`python` version: Python 3.5.3 (default, Sep 27 2018, 17:25:39) [GCC 6.3.0 20170516] on linux

💡 当前系统默认python为 3.5.3, 若想将系统默认python切换回python2, 运行以下命令然后跟随
指导操作.

```shell
sudo update-alternatives --config python
```

⚠️需注意pip的版本与python版本相匹配, 通过运行 `pip -V` 来查看pip版本和位置

`django` version: 2.1.7

# CAN转SPI模块

📖[RS485 CAN HAT用户手册](doc/CAN2SPI/RS485-CAN-HAT-user-manual-cn.pdf)

📖[RS485 CAN HAT电路图](doc/CAN2SPI/RS485_CAN_HAT_Schematic.pdf)

🔗 [python-can文档](https://python-can.readthedocs.io/en/master/index.html#)

# 车载网站 (交互平台)

本网站基于Django框架.

🔗 [Django中文文档](https://docs.djangoproject.com/zh-hans/2.1/)

## oncar

### oncar设计方针

📖 [oncar设计方针](doc/furyTerminal/oncar/设计方针.md)

## django纪要

### 设置允许访问的地址

在 `furyTerminal/furyTerminal/settings.py` 中 **ALLOWED_HOSTS**一项设置了允许访问
网站的地址, 设为 `'*'` 则是允许所有地址访问.

### 常用命令

#### 运行网站

⚠️ 在网站根目录执行.
💡此时为网站在 **localhost:8000** 运行

```shell
python furyTerminal/manage.py runserver 0:8000
```

#### 生成应用的迁移

```shell
python manage.py makemigrations [app]
```

#### 应用迁移到网站

⚠️ 在网站根目录执行.

```shell
python manage.py migrate
```

### 注意事项

- path()函数的参数`route`不会匹配 GET 和 POST 参数或域名。例如，URLconf 在处理请求
  https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ 。处理请求
  https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/。