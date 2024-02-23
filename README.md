# Scrapy
爬虫框架Scrapy的学习和使用

![scrapy.png](./assets/scrapy.png)

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

