---
title: Mac小技巧
date: 2016-02-29 16:07:14
tags:
 - oauth
---

### MacBook 电池
1. 如果当台式机用，每天插着电，一个月至少放电一次到20%
2. 如果长期闲置，维持50%的电量
3. 避免电量过低
4. 温度： 10 ~ 35 摄氏度

### 快捷键
cmd+shift+3,4 

### Mac域名中含有 Bogon
bogon表示不要路由到公网。但mac怎么会去反问DNS呢？

解决办法：

    sudo hostname [你的hostname]
    sudo scutil --set LocalHostName $(hostname)
    sudo scutil --set HostName $(hostname)

### Terminal 上个命令最后那个参数

    esc + .

    