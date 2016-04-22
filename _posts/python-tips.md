---
title: python相关
date: 2016-03-08 11:13:14
tags:
 - python
---

### encoding
import codecs
codecs.decode( obj, "gbk" )

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
 

### csv

csv.field_size_limit(sys.maxsize)

import csv
csv.reader(f)
csv.writer(f)
for row in reader:
    pass
writer.writerow([])


### Python

PYTHONPATH是Python搜索路径，默认我们import的模块都会从PYTHONPATH里面寻找。

### system
sys.version
sys.platform
sys.argv
sys.maxint

import re
dir(re) inspect module, object

### python type system
base type: object
primitive types: int, float, bool, long, complex
container type: tuple, string, unicode, list, set, fronzenset, dictionary
code type:
internal type:

immutable: tuple, string, unicode, fronzenset


isinstance(12, object)

### duck type
1 + 1 is syntax of 1.__add__(1)
[1,2,3][0] => [1,2,3].__getitem__(0)

isinstance(obj, type) vs duck type


### int float
max value: sys.maxint, sys.float_info
32bit cpu: 2**31 - 1, x64: 2**63 -1 

long: not bounded

literals 8 16 10 base: 0x123, 0123, 123

right:
2**2**3 = 2 ** ( 2 ** 3 )

10.1 // 2 == 5.0


### string unicode
string is ascii characters

unicode -> string:
u'或者'.encode('utf-8')
=> '\xe6\x88\x96\xe8\x80\x85'
string -> unicode
unicode('\xe6\x88\x96\xe8\x80\x85', 'utf8') => u'或者'

len(u'或者') == 2

### list map
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
letters[1]
if 'a' in letters:
    pass


map = { "name": "bob", "age":123 }
map["name"]
if "name" in map:
    pass

for k,v in map.iteritems():
    print k,v

### python bytecode
import dis

def f():
    pass
dis.dis(f)

### python debug

break 或 b 设置断点  设置断点
continue 或 c    继续执行程序
list 或 l    查看当前行的代码段
step 或 s    进入函数
return 或 r  执行代码直到从当前函数返回
exit 或 q    中止并退出
next 或 n    执行下一行
pp  打印变量的值
help    帮助

## yield
python bytecode:
YIELD_VALUE

return generator, can send back information
can't send non-None value to a just-started generator
send will trigger next value


### python pip

see package version:
pip show Flask
pip list

### Python numpy

### Python socket编程

int listen(int sockfd, int backlog)
默认时主动的，这个调用变成被动
backlog: OS 维护一个两个队列： 未连接的tcp队列（半连接），完成3次握手的tcp（准备好的）。准备好的tcp将交给进程（accept调用返回）； 为空则睡眠。

backlog = 0， 可能引发 tcp flooding

防止 tcp flooding:
使用F5，原理是完成3次握手的，才转发到服务器，有效阻挡半连接攻击
修改/etc/sysctl.conf, tcp_synack_retries = 0 即没收到客户端到ack，不重试；net.ipv4.tcp_max_syn_backlog = 200000 设置总到连接数

socket状态：
开始连接：
listen
syn_sent
syn_rcvd
established
主动close:
fin_wait_1
fin_wait_2
closing
time_wait
被动：
close_wait
last_ack
关闭：
closed





### pyspark

代码模板：

    import sys 
    from pyspark import SparkContext 
    if __name__ == '__main__':
        sc = SparkContext() #远程提交任务，采用默认配置 
        argv = sys.argv 
        src = argv[ len(argv)-2 ] 
        dst = argv[ len(argv)-1 ]

[pyspark doc](https://spark.apache.org/docs/1.3.1/api/python/pyspark.html)

### 文档编码

指定文档编码

    # -*- coding: encoding -*-

### 异常处理

        try:
            line = raw_input()      #从stdin读入行
        except EOFError:
            break                #在文件末尾退出循环
        esle:
              # 其它处理代码

抛出异常：

    raise BaseException("error")

### map

遍历：

    m = dict()
    for k,v in m.iteritems():
        print k,v

key，value相关操作

    map.get("key1") # 如果key、value对不存在，不会抛出异常
    map["key1"] # 可能抛出 KeyError 
    key in map # 检查key,value对是否存在


### 命令行

执行一段代码：

    python -c ‘print 123'
    python m1.py
    python -m m1 比如当前文件夹下有一段代码 m1.py，这样将直接执行这个文件； 和 python m1.py效果一样。

#### 命令行参数传递

t.py:

    import sys
    print sys.argv 
执行python t.py 123 124，打印：注意包含文件名本身

    [ ’t.py’, ‘123’, ‘124' ]

执行：

    python -c “import sys; print sys.argv” 123
    
打印：

    [‘-c', ‘123']

### 基本运算

向下取整的除法：
 
    4/5 == 0
    4.0 // 5 == 0 强制向下取整除法，即使是浮点数

求幂运算
    
    2**3

交互运算时，用_表示前一个结果

### 字符串
可以相加：

    ‘a’ + ‘b'

重复：
    
    ‘a’*3

多行： 注意没有前导的换行

    “””\
    abc
    def
    “”"
用\转义

    “this is \n a new line"

或者取消\转义功能

    r“c:\a\b"

多个相邻的字符串常量（变量不行），自动拼接

    a = ‘a’ ‘b'

字符串索引：

    a[0]
    a[1]
    a[-1] = a[len(a)-1]

切片：

    a[0:1]
    a[1:]
    a[:1]
    a[start:end_not_included]

如果省略start，默认为0； 省略 end，默认为字符串长度
a[too_large]太大的索引，会报错
但是切片不会，根据情况，适配到 [start:end] 之间来。


字符串不可变：
    
    a[0] = ‘1’会失败

求长度
    
    len(str)

### 类

    class A:
      def __len__(self):
         return 102
      @classmethod
      def joke(cls):
          return “a class method %s” % cls
    a = A()
    print a.__len__()
    print A.__len__(a)
    print len(a)
    print A.joke()

