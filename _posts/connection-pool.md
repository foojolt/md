---
title: 数据库连接池配置参考
date: 2016-03-05 07:07:14
tags:
 - 连接池
---

连接池的出现，是由于建立数据库连接花费较大，包括TCP三次握手、连接初始化、DB端资源准备等；
而且系统要控制连接的数量，防止资源耗尽。

主要的一些配置项：
maxTotal 连接池最大容量
maxIdle 最大空闲数
minIdle 最小空闲数
maxUseMillis 连接池签出后，连接最长使用时间
validateSql 校验连接是否有效的sql语句，一般是select 1
validationQueryTimeout 校验语句最长执行时间
testWhileIdle 空闲时调用validateSql检查
timeBetweenEvictionRunsMillis 空闲时校验间隔（如果testWhileIdle为false，则不校验直接删除）

考虑一些异常场景：
E1. 高并发，即达到 maxTotal；签出连接是否阻塞，是否支持超时
E2. 数据库重启；
E3. client和DB之间，有防火墙，且防火墙设置了tcp的最长空闲时间；
原连接失效，且client和DB都不知道。
E4. 网络延迟，建立tcp和数据传输耗时严重；解决： 超时配置。

### 常见连接池实现
1. Apache DBCP: 底层使用 commons-pool2 的 GenericObjectPool 对象池实现。
实现类是 BasicDataSource，比较常见。
2. Alibaba Druid：除了DBCP提供的常用功能外，通过filter-chain的方式支持了一些额外的功能，
如Sql运行监控StatFilter，可以配置servlet在网页上查看。
由于StatFilter使用了自己实现的SQLParser，能提供更详细的运行信息。
3. C3P0

### 常见异常处理

#### E1： 签出超时：
    Druid支持maxWait(默认0)，在在达到 maxTotal（maxActive）之后，线程的阻塞等待时间。
    C3P0支持：checkoutTimeout
    DBCP是一直阻塞，不支持超时

#### E2：DB重启，原有连接均失效；在重启期间，获取连接会失败：

1. 是否支持失败重试：
    C3P0通过以下属性支持重试：
    acquireRetryAttempts:30 重试几次
    acquireRetryDelay:1s 重试间隔
    breakAfterAcquireFailure:false 重试失败后，后续是否都失败；
    DBCP 和 Druid不支持重试配置。

2. 是否支持失效连接检测和删除：
    3个实现均支持签出检测、归还检测、以及 testWhileIdle(C3P0是idleConnectionTestPeriod)

#### E3: client和DB之间有防火墙
防火墙可能设置有TCP超时，会使client和DB之间的TCP连接失效，而双方都不知道。
1. 可以通过心跳维持连接
    3个实现均支持 testWhileIdle
2. 可以使 idle 连接失效。
    3个均支持




不足：
1. 官方的文档上，没有出现validationQueryTimeout配置，虽然底层支持。
2. 与 BasicDataSource 一样，不支持底层 connection的超时配置。



其他：
1. Druid



end。
