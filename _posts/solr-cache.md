---
title: Solr Cache
date: 2016-03-07 11:07:14
tags:
 - solr
 - cache
---

### 基本概念

三种类型的缓存：

    filter-query-cache, query-cache, document-cache

一个query cache缓存占用内存估计： 
    
    查询字符串本身占 80 byte
    平均每个查询返回 10000 个结果，每个结果就是 8 byte（document id）, ~ 80KB

一个 filter cache缓存占用内存估计： 
    
    查询字符串本身占 80 byte
    假设共有100万偏文档，用一个bit表示一个文档，需要 100万/8 = 125 KB
    保存1000个fq缓存，需要 120MB内存

### filter cache

假设有filter query查询：

    /select?q=velvet+pants&fq=category:apparel

与组合查询的区别：

    /select?q=(velvet+pants)+AND+category:apparel

1. fq 本身不会改变最终排序结果，而AND查询会
2. 可以使用 velvet+pants 的 query cache
3. 可以使用 category:apparel 的 filter cache
4. 有一个或多个fq存在的情况下，先进行fq

documnet cache 就是 document id 到 document 对象的映射。不如 query cache 和 filter cache 那么有效。

### 增加缓存的考虑

1. OS本身有文件系统缓存，分配的内存是从OS抢过去的
2. 缓存过大，增加JVM GC压力

### 缓存性能

主要指标：
    
    cumulative_inserts
    cumulative_evictions
    cumulative_hitratio

### Solr 空间搜索

GeoHash: 将纬度和经度用二进制表示： 类似二分查找，每次根据落在二分的哪边标记为0或1，越分越细； 错位将经度和纬度放在一起；用类似base64编码。
问题：边界点可能hash的字符串会差别较大，搜索时，需要同时检索周边8个点。

http://tech.meituan.com/solr-spatial-search.html


### 问题

1. 为什么 query cache 和 fq cache 用的缓存记录方式不一样？
2. 每一种cache的key 和 value ?
3. 


### 参考

[Solr cache tuning](https://teaspoon-consulting.com/articles/solr-cache-tuning.html)
