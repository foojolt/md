---
title: Redis 及缓存
date: 2016-03-17 10:07:14
tags:
 - redis
 - 性能
---

### Redis其他



###LRU

maxmemory 2G
maxmemory-policy allkeys-lru
maxmemory-samples 10

redis的行为是在每次add key之后，检查是否超过 max memory, 超过则启动一个 sample 算法，去除更老的key.

### 缓存系统

redis特点：
1. binlog， 故障恢复
2. 持久化
3. 内存放不下，可以LRU写到文件中

### Redis单线程

Redis is single-threaded with epoll/kqueue and scales indefinitely in terms of I/O concurrency

CPU 不是瓶颈， IO和内存才是

### Partition

缺点：
1. 批量key操作不可行
2. 批量key事务不可行
3. 基于key而不是value来做的，value很大也不能

分片方式：
client-side： 客户端手工配置
proxy： 代理分片
clustering： 没有中心点，类似cassendra， 每个节点都纪录其他接点的信息；出了问题不好定位；

twemproxy: 

codis: 
1. codis group概念（ 包含至少一个master/slave)
2. pre-sharding: 1024个分片，分片信息保存在zookeeper中
redis-client -> codis proxy...-> [ codis-grp1 (redis-master, redis-slave1, redis-slave2,...) , codis-grp2,... ]

### Redis Cluster

分为 16384 个槽，每个shard领取一部分；  16 * 1024 = 16384
用bitmap存储 node 和 shard的对应信息 （2K的bitmap）

### Redis-Sentinel

redis官方HA机制： 实现了一个类似 zookeeper 的主备选举机制
数据要写到master，读可以从slave读； 延时 ＋ 分裂时的数据丢失

Sentinel 和 redis 节点分开部署，至少3个

asynchronous replication 异步复制

Sentinel or Clustering:

看情况，如果要求HA（即里面的数据很重要，在一段时间内不能丢失），用sentinel
所有节点存储的是相同的key-value

如果只是做缓存，故障之后可以重建； 用 partition 的方案。

### 一致性哈希与缓存

分布式哈希的实现： 环状＋就近存储
根据 hash(node_ip) 分布缓存的node
hash(key)并顺时针找到最近的node

1. 平衡性： 均匀分布
2. 单调性： 缓存node增加和删除，只有部分key需要迁移
3. 平衡性： 虚拟node，hash(node_ip#1),hash(node_ip#2) ...

http://blog.csdn.net/cywosp/article/details/23397179

