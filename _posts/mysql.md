---
title: Mysql Essentials
date: 2016-03-17 10:07:14
tags:
 - mysql
 - 事务


### Mysql 事务

两阶段锁：
加锁阶段： 读取共享锁（S锁）， 写入排他锁（X锁）
释放阶段：

隔离级别：
未提交读(Read Uncommitted)：允许脏读，也就是可能读取到其他会话中未提交事务修改的数据
提交读(Read Committed)：只能读取到已经提交的数据。Oracle等多数数据库默认都是该级别 (不重复读)
可重复读(Repeated Read)：可重复读。在同一个事务内的查询都是事务开始时刻一致的，InnoDB默认级别。在SQL标准中，该隔离级别消除了不可重复读，但是还存在幻象读
串行读(Serializable)：完全串行化的读，每次读都需要获得表级共享锁，读写相互都会阻塞

不可重复读： 针对update和delete
幻读：针对insert操作，可以读到之前不存在的记录

mysql锁的类型： 行锁， 表锁

SET session transaction isolation level read committed;
SET SESSION binlog_format = 'ROW';（或者是MIXED）

行锁： 
update where id=xxx 行加锁
update where non_id = xxx 表锁 （mysql可能违反两阶段原则，在发现满足条件时，释放有关行；但由于没有索引，效率也不高）

mysql在 read committed 级别， 读操作不会加锁；

解决不可重复读／脏读读问题： 乐观锁， 多版本并发控制 mvcc， multi-version concurrent control

mysql mvcc: 在每一行的后面， 增加两个隐藏的值： 创建事务id （insert/update） 和过期事务id(update/delete)

SELECT时，读取创建版本号<=当前事务版本号，删除版本号为空或>当前事务版本号。
INSERT时，保存当前事务版本号为行的创建版本号
DELETE时，保存当前事务版本号为行的删除版本号
UPDATE时，插入一条新纪录，保存当前事务版本号为行创建版本号，同时保存当前事务版本号到原来删除的行

update会新建一条记录

快照读和加锁读
mysql引入快照读，提升性能

next-key 锁： 行锁和gap锁的结合体
gap锁防止区间插入，从而防止了幻读的问题。













