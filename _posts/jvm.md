---
title: Jvm 性能分析
date: 2016-03-14 11:07:14
tags:
 - jvm
 - 性能
---

### 性能分析方法

自顶（APP）向下 自底（CPU／内存）向上

### CPU相关
vmstat 主要观察调度队列度大小，cpu interrupt/context switch, cpu usage等相关数据

### 锁
http://www.infoq.com/cn/articles/java-se-16-synchronized
CAS compare and swap 
同步的原理： monitor 对象
锁状态存储在对象头中

锁的升级： 
偏向锁，默认开启，因为发现大部分情况下，锁都是由同一个线程获得
自旋锁，不会阻塞，需要轮询；在多核CPU的情况下，可以避免让步上下文切换
重量级锁，线程阻塞

### CAS

compare and swap: 用在 atomic, incrementAndGet， 循环比较

AtomicReference 可以用来实现无锁的Stack等。

CAS循环探测的问题：
1. 在并发较高时，多数线程在探测，影响性能
2. 有时候compare返回true，可不能swap，可能状态已经变了（比如一个stack只保存head，实际上同一个head插入来两次）

### 并发和并行

Concurrency: A condition that exists when at least two threads are making progress. A more generalized form of parallelism that can include time-slicing as a form of virtual parallelism. 逻辑上

Parallelism: A condition that arises when at least two threads are executing simultaneously.  物理上的

### 类加载
bootstrap classloader
ext classloader
system classloader

初始化加载器： loadClass() 会掉用findClass,比如URLClassLoader，如果没找到资源，直接跑出classNotFoundException

定义类加载器: defineClass() 通过读取 byte[]，如果发现没有指定的类定义，则抛出NoClassDefFoundError

线程上下文加载器：应对SPI的场景。

Class.forName:简便方法
>Class<?> caller = Reflection.getCallerClass();
return forName0(className, true, ClassLoader.getClassLoader(caller), caller);
>附： jdbc4以前，需要 Class.forName来加载指定的Driver，因为这样会初始化这个类：Driver就是这个时候，将自己注册到DriverManager的；jdbc4在DriverManager.getConnection getDrivers方法中，会去找 services/java.sql.Driver文件并加载所有的Driver，需要用到线程上下文类加载器

链接：
验证 可能抛出VerifyError
准备 准备静态域并设为默认值
解析 处理符号表中有其他的类引用，可能导致其他类被加载

初始化：
初始化静态域和执行静态代码

### jvm线程管理

线程模型： 和OS线程一一对应

两种方式创建线程：  
new Thread().start(): JavaThread(C++) -> OSThread
attach一个本地线程到jvm: 比如 CreateVM 时，是首先创建一个本地线程，做必要的初始化之后，再attach

从JVM角度看Thread State:
new, in_java, in_vm, blocked( monitor_wait, condition_var_wait, object_wait )

安全点：
比如GC的时候

### JVM C++ heap manage
Arena ChunkPool 自定义的内存分配，而不是 malloc

###JVM致命错误处理

-XX:ErrorFile=
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=<pathname>

### jvm参数

标准参数，扩展参数，不稳定的参数

PERM | OLD | NEW[eden ss1 ss2]

-Xloggc:filename
-Xms:初始堆大小
-Xmx:最大堆大小
-XX:NewSize=n:设置年轻代大小
-XX:NewRatio=n:设置年轻代和年老代的比值。如:为3，表示年轻代与年老代比值为1：3，年轻代占整个年轻代年老代和的1/4
-XX:SurvivorRatio=n:年轻代中Eden区与两个Survivor区的比值。注意Survivor区有两个。如：3，表示Eden：Survivor=3：2，一个Survivor区占整个年轻代的1/5
-XX:MaxPermSize=n:设置持久代大小

### 常见诊断工具
 jinfo pid 获取jvm的启动参数
 jmap －heap pid
 jmap -dump:live,format=b,file=heap.bin pid live表示先gc
 jstack pid

 jstat -gcutil pid time_range sample_count
 S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   



### vmstat 命令解析

CPU:
---
r 调度队列的大小，参考cpu核数
b 阻塞的任务数

Memory: 
---
swapd 交换内存大小
free
buff 
cache

Swap:
----
si
so

io
----
bi
bo

system 
----
in (interrupt per second)
cs (context switch per second)

cpu
----
us
sy
id
wa (time wait for io)
st (unknown)



top -H -p pid 查看线程
pstree -p pid 查看线程



### 参考

《Java性能调优》