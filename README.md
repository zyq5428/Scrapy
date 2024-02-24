# Scrapy
爬虫框架Scrapy的学习和使用

![Scrapy框架图.png](./assets/Scrapy框架图.png)

* Scrapy Engine(引擎): 负责Spider、ItemPipeline、Downloader、Scheduler中间的通讯，信号、数据传递等。
* Scheduler(调度器): 它负责接受引擎发送过来的Request请求，并按照一定的方式进行整理排列，入队，当引擎需要时，交还给引擎。
* Downloader（下载器）：负责下载Scrapy Engine(引擎)发送的所有Requests请求，并将其获取到的Responses交还给Scrapy Engine(引擎)，由引擎交给Spider来处理，
* Spider（爬虫）：它负责处理所有Responses,从中分析提取数据，获取Item字段需要的数据，并将需要跟进的URL提交给引擎，再次进入Scheduler(调度器).
* Item Pipeline(管道)：它负责处理Spider中获取到的Item，并进行进行后期处理（详细分析、过滤、存储等）的地方。
* Downloader Middlewares（下载中间件）：你可以当作是一个可以自定义扩展下载功能的组件。
* Spider Middlewares（Spider中间件）：你可以理解为是一个可以自定扩展和操作引擎和Spider中间通信的功能组件（比如进入Spider的Responses;和从Spider出去的Requests）

## 入门教程

创建一个 Scrapy 项目，项目文件可以直接用 scrapy 命令生成，命令如下所示：
    scrapy startproject tutorial
这个命令将会创建一个名为 tutorial 的文件夹，文件夹结构如下所示：
``` {.line-numbers highlight=[2]}
scrapy.cfg     # Scrapy 部署时的配置文件
tutorial         # 项目的模块，引入的时候需要从这里引入
    __init__.py    
    items.py     # Items 的定义，定义爬取的数据结构
    middlewares.py   # Middlewares 的定义，定义爬取时的中间件
    pipelines.py       # Pipelines 的定义，定义数据管道
    settings.py       # 配置文件
    spiders         # 放置 Spiders 的文件夹
    __init__.py
```

使用命令行创建一个 Spider。比如要生成 Quotes 这个 Spider，可以执行如下命令：
    cd .\tutorial\
    scrapy genspider quotes quotes.toscrape.com
第一个参数是 Spider 的名称，第二个参数是网站域名。执行完毕之后，spiders 文件夹中多了一个 quotes.py，它就是刚刚创建的 Spider。
这里有三个属性——name、allowed_domains 和 start_urls，还有一个方法 parse。
* name：它是每个项目唯一的名字，用来区分不同的 Spider。
* allowed_domains：它是允许爬取的域名，如果初始或后续的请求链接不是这个域名下的，则请求链接会被过滤掉。
* start_urls：它包含了 Spider 在启动时爬取的 url 列表，初始请求是由它来定义的。
* parse：它是 Spider 的一个方法。默认情况下，被调用时 start_urls 里面的链接构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数。该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求。

关闭robot规则检查(settings.py)
    ROBOTSTXT_OBEY = False

运行爬虫：
    scrapy crawl quotes

