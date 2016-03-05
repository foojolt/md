---
title: 写程序判断闰年
date: 2016-02-29 17:07:14
tags:
 - python
 - 闰年
---

今天很特殊，2月29日。写一篇相关的内容：写程序判断闰年

### 简单的问题不简单

闰年:
>四年一闰，百年不闰，四百年再闰

### 第一个版本

{% codeblock lang:python %}

def is_leap_year(year):
  if year % 400 == 0:
    return true
  elif year % 100 == 0:
    return false
  elif year % 4 == 0:
    return true
  return false

{% endcodeblock %}
上面的写法有什么问题？
（1） 太长了，不够优雅
 (2) 应该从4开始判断，再到100，再到400；这样判断的次数就少多了。

### 第二个版本

{% codeblock lang:python %}

def is_leap_year(year):
  return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

{% endcodeblock %}
### python中的 and or
a = x1 and x2 and x3 and ...
a的值，等于第一个为false的x的值；或者最后一个x的值。
b = y1 or y2 or y3 or ...
a的值，等于第一个为true的y的值；或者最后一个y的值。

因此：
> and 或 or 表达式的值，不是布尔类型的，和操作数有关
