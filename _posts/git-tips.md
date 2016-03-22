---
title: Git技巧
date: 2016-03-01 11:07:14
tags:
 - git
---

#### 查看某个文件的历史版本内容：

最常用的，往回查看一个版本：
    git show HEAD~1:_posts/connection-pool.md

或者用git log，查看历史记录之后，附上版本号查看：

git show e9468eca43385f7d3b9ade9cb585bec05f1a6846:_posts/connection-pool.md
