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

2. 下载最新版本的压缩包 [release](https://github.com/Jacken-Wu/Erling/releases) 并解压；
3. 第一次运行时先运行初始化程序 init.py，设置数据文件存储路径（注：输入的路径必须是已存在的路径，否则会报错），若要更改数据文件存储路径，可以编辑程序目录中的 data_path.config 文件，或再次运行 init.py，再次运行init.py 文件时已有数据不会被重置，但以防万一请在运行 init.py 前先备份；
4. 配置数据文件存储路径下的 constant.config 文件，其中百度翻译的 appid 和 key 自行申请，如不需要此功能则忽略此项设置；
5. 分别运行 main.py 和 send_notice.py，Linux 用户可使用 screen 命令使二者运行在后台，如不需要定时提醒、定时发送消息等功能可以不运行 send_notice.py。

### 词向量和对话训练

对话功能使用 词向量+语料库 匹配的方式，回答相对单一，但能满足基本的对话需求。

1. 词向量训练请调用 chat.py 中的 generate_vec() 函数，运行前请将训练文本放在数据文件存储路径（默认 ./data/）下的 trainning/text 文件夹内，训练好的模型为 model_word2vec 文件；
2. 对话库生成请调用 chat.py 中的 generate_conversation() 函数，运行前请将训练文本放在数据文件存储路径（默认 ./data/）下的 trainning/conversation 文件夹内，生成的对话库为 database_conversation.yml 文件；

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
