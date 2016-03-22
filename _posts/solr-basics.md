---
title: Solr基础
date: 2016-03-07 11:07:14
tags:
 - solr
---

### 命令行

./solr-5.5.0/bin/solr delete -c fslink
./solr-5.5.0/bin/solr create_core -c fslink -d fslink-solr-core/

### 基础概念

基本概念：

    Document：代表一篇文档，相当于数据表的一行记录
    Field：文档的属性，相当于数据表的列。一个Document包含一个或多个列。
    Index：索引，这里指倒排索引，一个 Index包含一个或多个 Document

Schema：在索引Document之前，需要给出一个schema.xml文件，用于描述：

    Document有哪些Fields，类型是什么
    哪个Fields是主键
    哪些Fields是必须的
    如何索引和查询Fields

Field的类型：支持自定义类型

    float,double,long,date,text

定义一个Field：
    
    name：名称
    type：类型
    indexed：是否加入倒排索引
    store：是否保存原文
    multiValued：是否包含多值

Analysis过程：

    indexed：true 的Fields，都要经过一系列的分词、过滤等过程。也只有index过的field，才能参与搜索

是否保存：

    保存Fields的原始内容（而不是Analysis之后的值）,会增加索引文件的大小，从而降低查询速度。
    一个 indexed:false 的字段，也可以 stored: true

与 lucene的关系：

    lucene是solr的内核引擎

core:
    
    solr core 代表一堆的配置文件（solrconfig.xml schema.xml）、 事务处理的log、 以及索引文件。 多个core可以加载到同一个solr实例中。 

### Solr的查询语法

基本的匹配：一个、多个关键词，多个Field匹配，多个条件组合

    title:foo
    title: "foo bar"
    title: "foo bar" AND body: "fox"
    ( title: foo ADN body: fox ) OR title:fox
    title:foo and -title:fox

模糊匹配：* 表示0个或多个任意字符

    title:foo*
    title:foo*bar

距离匹配：两个单词的距离差4个单词以内，需要Solr DisMax 或 eDisMax 查询分析器

    title:"foo bar"~4

范围匹配：

    mod_date:[ 201301 TO 201407 ]

Boosts: 可以人为设定哪个关键词更重要，影响结果文档的排序

    (title:foo OR title:bar)^1.5 (body:foo OR body:bar)

其他与lucene之外的功能：

    field:[* TO 100]
    field:[100 TO *]
    field:[* TO *]
    -inStock:false 只包含一个非条件
    -field:[* TO *] 某个field没有值
    _val_:"recip(rord(myfield),1,2,3)" 指定查询函数
    _query_:"{!dismax qf=myfield}how now brown cow" 指定query parser

### 实例研究

启动一个样例：

    bin/solr -e techproducts
    这个命令启动了solr:8983，并将一些文档加入索引

配置文件地址： example/techproducts/solr/techproducts/conf/managed-schema

    bin/solr status 查看状态

    cd example/exampledocs
    java -Dc=techproducts -jar post.jar sd500.xml 本地索引文件

两种方式添加索引：

    HTTP
    Native client

查询：可以指定获取那些字段
    
    http://localhost:8983/solr/techproducts/select?q=sd500&wt=json
    http://localhost:8983/solr/techproducts/select?q=inStock:false&wt=json&fl=id,name

### 配置

    solrconfig.xml 配置dataDir requestHandler cache等（包括DefaultSearchField的配置）
    managed-schema 定义schema，支持动态字段，支持copy-field


### 问题

1. 点击solr admin界面上的 optimize， 做了什么事情？
2. 那几个缓存是什么意思？ [solrconfig](http://www.solrtutorial.com/solrconfig-xml.html#cache)
3. facet 查询的概念, 以及其他的查询方式？
4. 
### 其他 

[Solr ElasticSearch对比](http://solr-vs-elasticsearch.com)

### 参考

[ Toturial](http://www.solrtutorial.com/solr-query-syntax.html)



end
