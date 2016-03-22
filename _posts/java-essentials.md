---
title: Java有趣知识
date: 2016-03-14 11:07:14
tags:
 - java
---


### 内存映射

MappedByteBuffer:

从 FileChannel创建， 可以是 RandomAccessFile，支持读写； 模式可以是 只读／读写／私有， 私有的修改不会刷回文件中。


### IO

linux io 模型
               blocking    non-blocking
               -------------------------
synchronous  | old io       app多次请求，直到条件满足
asynchronous | select/epoll       AIO

select 与 old io 的区别： old io是对IO调用阻塞； select 是对事件通知阻塞

nodejs使用libeio，默认内部使用4个IO线程。

select/poll，都是提供一堆fd和关心的事件给内核；然后循环阻塞探测到状态变化时，再逐个检查原来的fd，看看哪个有变化；
poll和select的区别：用了一个结构体；没有1024数量限制
epoll返回有变化的fd集合。而且不用每次拷贝fd到内核（后续调用使用 epollfd ）

java: bio, nio, aio(jdk7)

AIO: app侧提供buffer,回调函数callback； callback在内核栈上执行
API：
aio_read    请求异步读操作
aio_error   检查异步请求的状态
aio_return  获得完成的异步请求的返回状态
...

https://www.ibm.com/developerworks/cn/linux/l-async/

### netty

channel -> channel pipeline -> channelHandlers 

network read -> upstream handlers 
io request -> downstream handlers -> sink

netty 3的问题： 每次有IO消息，就产生event，增加GC时间
netty 4: 不在包装event，而是调用相应的接口处理方法； 开发自己的malloc，不用填充0；自己管理，减少gc

https://m.oschina.net/blog/178561

### 线程池

行为：
coreSize -> taskQueue -> maxSize
只要coreSize没有达到，就创建新的线程；
否则任务进队列: 判断offer是否返回true;
进队列失败，且 < maxSize，创建新的线程；
否则，调用 handler处理。

newFixedThreadPool: core==max, 无边界的 LinkedBlockingQueue，只要大于core，就无限制排队
newCachedThreadPool: SynchronousQueue，执行任务为0，立即入队列；否则失败，创建新的线程执行任务。
ArrayBlockingQueue: 考虑用这个，一旦队列满，就停止入队；降低系统负载；

### 内存模型

内存模型确定了一些规则：线程对内存的访问如何排序，以及如何确保内存对线程可见
包括： 重排序，内存可见性，happens-before

重排序包括： 编译器重排序 CPU重排序 缓存导致的写入主内存重排序

可见性： 内存屏障实现

happens-before法则：
－ 程序次序法则：线程中的每个动作A都happens-before于该线程中的每一个动作B，其中，在程序中，所有的动作B都能出现在A之后。
－ 监视器锁法则：对一个监视器锁的解锁 happens-before于每一个后续对同一监视器锁的加锁。
－ volatile变量法则：对volatile域的写入操作happens-before于每一个后续对同一个域的读写操作。
－ 传递性：如果A happens-before于B，且B happens-before于C，则A happens-before于C
－ 对final语义的扩展保证一个对象的构建方法结束前，所有final成员变量都必须完成初始化（的前提是没有this引用溢出）。
－ 线程启动法则：在一个线程里，对Thread.start的调用会happens-before于每个启动线程的动作。
－ 线程终结法则：线程中的任何动作都happens-before于其他线程检测到这个线程已经终结、或者从Thread.join调用中成功返回，或Thread.isAlive返回false。
－ 中断法则：一个线程调用另一个线程的interrupt happens-before于被中断的线程发现中断。
－ 终结法则：一个对象的构造函数的结束happens-before于这个对象finalizer的开始。

一个volatile happens-before原则的应用：
class VolatileExample {
    int x = 0;
    volatile boolean v = false;
    public void writer() {
        x = 42;
        v = true;
    }
    public void reader() {
        if (v == true) {
            //uses x - guaranteed to see 42.
        }
    }
}

### BlockingQueue

offer和poll提供超时参数

### CopyOnWriteArrayList
每次修改，都创建一个新的底层Array: 读的线程，拿到的可能是失效的快照


### ConcurrentHashMap

Map is list of Segment
    Segment is list of HashEntry

用分离锁实现多个线程间的并发写操作
用 HashEntery 对象的不变性来降低读操作对加锁的需求
用 Volatile 变量协调读写线程间的内存可见性（value是volatile的，保证写入之后可以被其他线程看见；修改之后，改变volatile的modCount）

HashEntry 是一个为无锁读优化的链表： 
value 是volatile，表示如果读的时候正在改写能立即体现
next 是final，表示只能往前插入节点： 拿到一个hashEntry，它的链表元素是固定的（value除外）

 static final class HashEntry<K,V> { 
        final K key;                       // 声明 key 为 final 型
        final int hash;                   // 声明 hash 值为 final 型 
        volatile V value;                 // 声明 value 为 volatile 型
        final HashEntry<K,V> next;      // 声明 next 为 final 型 

        HashEntry(K key, int hash, HashEntry<K,V> next, V value) { 
            this.key = key; 
            this.hash = hash; 
            this.next = next; 
            this.value = value; 
        } 
 }























