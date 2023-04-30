# 二澪(Erling)

## 目录

[描述](#描述)  
[工作目录](#工作目录)  
[运行逻辑](#运行逻辑)  
[使用说明](#使用说明)  
[二澪人设](#二澪人设)  

## 描述

本项目为某VOCALOID群的群聊机器人python代码。  

## 工作目录

├── bot_func  /自定义库  
├── init_files  /初始化文件  
├── init.py  /初始化程序  
├── main.py  /主程序  
└── send_notice.py  /定时发送消息的程序  

## 运行逻辑

### main.py

1. 从本地端口5701获取消息字符串；
2. 对消息字符串处理，得到的消息json；
3. 判断消息类型和发送者；
4. 处理消息，根据消息特征选择如何处理。

### send_notice.py

* 整个程序是一个循环，每次循环时判断是否达到定时的时间，若达到则发送相应的信息。

## 使用说明

### 首次使用

1. 使用前请下载并运行 [go-cqhttp](https://docs.go-cqhttp.org/guide/quick_start.html)，如下所示配置 HTTP 通信

    ``` yml
    - http:
        address: 127.0.0.1:5700
        ...
        post:
        - url: 'http://127.0.0.1:5701'
            secret: ''
            max-retries: 0
    ```

    端口号可更改，对应 main.py 以及 bot_func/send.py 代码中的端口号也改为相应值；

2. 安装任意版本的 python3 并安装以下 python 库: numpy, jieba, gensim, lxml，若运行报错提示 import 找不到库，就 pip 安装对应的库；
3. 安装ffmpeg，windows用户请手动添加ffmpeg安装路径到环境变量；
4. 下载最新版本的压缩包 [releases](https://github.com/Jacken-Wu/Erling/releases) 并解压；
5. 第一次运行时先运行初始化程序 init.py，设置数据文件存储路径（注：输入的路径必须是已存在的路径，否则会报错），若要更改数据文件存储路径，可以编辑程序目录中的 data_path.config 文件，或再次运行 init.py，再次运行init.py 文件时已有数据不会被重置，但以防万一请在运行 init.py 前先备份；
6. 配置数据文件存储路径下的 constant.config 文件，其中百度翻译的 appid 和 key 自行申请，如不需要此功能则忽略此项设置；
7. 分别运行 main.py 和 send_notice.py，Linux 用户可使用 screen 命令使二者运行在后台，如不需要定时提醒、定时发送消息等功能可以不运行 send_notice.py。

### 注意事项

* 更新方法：下载最新的 release 的压缩包，解压覆盖当前程序即可；
* 更新新版本后最好先删除 data 目录下的 constant.config 并重新运行 init.py，再次配置 constant.config。

### 指令

#### 管理员私聊指令

* help  
    help指令，发送help + 指令名字 可查看使用格式

* 提醒查看
* 提醒添加
* 提醒删除  
    查看、添加、删除定时提醒

* 记账支出
* 记账收入
* 记账查看
* 记账删除
* 记账备份  
    记账功能，账本文件为account，在数据存储目录下，记账备份文件为account + 日期，与账本在同一目录下

* 推歌添加
* 推歌查看
* 推歌删除  
    推歌功能，其实是定时发送群聊消息，除了用来定时推歌外，也可以用于发送其他的定时消息

* 添加歌曲  
    为曲库添加歌曲

* erlove  
    查看love值（用户可凭love值在“商店”购买物品，解锁各种功能权限）

* 通过好友  
    处理好友邀请

* 生成对话
* 重加载对话
* 生成词向量  
    如字面意思，是对话功能的处理指令

    对话功能使用 词向量+语料库 匹配的方式，回答相对单一，但能满足基本的对话需求。除上述指令外，还可直接在本地生成词向量模型和对话文件，如下：

    1. 词向量训练请调用 chat.py 中的 generate_vec() 函数，运行前请将训练文本放在数据文件存储路径（默认 ./data/）下的 trainning/text 文件夹内，训练好的模型为 model_word2vec 文件；
    2. 对话库生成请调用 chat.py 中的 generate_conversation() 函数，运行前请将训练文本放在数据文件存储路径（默认 ./data/）下的 trainning/conversation 文件夹内，生成的对话库为 database_conversation.yml 文件。

#### 群聊指令

[群聊指令介绍网页](https://jacken-wu.github.io/Erhelp/)

#### 普通用户私聊指令

* 添加歌曲

#### 私聊卡用户私聊指令

* help
* 提醒添加
* 推歌查看
* 推歌删除
* 添加歌曲  
    均与管理员私聊指令相同，添加的歌曲不会直接加入歌曲库，而是会推送给管理员

## 二澪人设

名字：二澪（Elling）  
身高：160cm  
体重：不详  
年龄：17  
印象色：浅蓝  
~~西巴，我一直把二澪的英文名记错成Erling了，项目名字就叫Erling~~  
~~明明是我自己好不容易起的名字，就当这个项目的二澪是真二澪的分身好了~~  

![erling1](https://i0.hdslb.com/bfs/album/9bd124359cc2f015135322b4516ca219c44d8ed8.png@1036w.webp)
![erling2](https://i0.hdslb.com/bfs/new_dyn/7af4a311826cecfb2646458d317e9560229017508.png@1036w.webp)
![erling3](https://i0.hdslb.com/bfs/new_dyn/55e0374fba234f38edcbd7cc087f48cd229017508.png@1036w.webp)
![erling](https://i0.hdslb.com/bfs/new_dyn/dfc9ce61afe92d39198168745a69b7a5229017508.png@1036w.webp)
