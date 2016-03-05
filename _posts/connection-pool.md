---
title: 数据库连接池配置参考
date: 2016-03-05 07:07:14
tags:
 - 连接池
---

连接池的出现，是由于建立数据库连接花费较大，包括TCP三次握手、连接初始化、DB端资源准备等；
而且系统要控制连接的数量，防止资源耗尽。

本文关注的一些配置项，名称可能有差异：
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
E2. 数据库重启；原连接失效，在idle状态、或签出时，能否检测并处理
E3. client和DB之间，有防火墙，且防火墙设置了tcp的最长空闲时间；
原连接失效，且client和DB都不知道。
E4. 网络延迟，建立tcp和数据传输耗时严重；超时配置，是否支持底层连接池超时配置

### DBCP.BasicDataSource

BasicDataSource 是 apache-commons的子项目，底层使用 commons-pool2 项目的
GenericObjectPool对象池.

特点和默认配置：
1. maxTotal: 8, maxIdle: 8, minIdle: 0, initialSize: 0
2. 支持 idle状态和签出时，检测和删除失效连接，返回下一个可用连接（需要时创建新的连接）
默认 testOnBorrow: true, testWhileIdle: false
3. 支持空闲时检查和删除失效连接。如果minIdle>0，则出现E3异常，可以让client定期发送
数据包，让防火墙以为tcp连接还活着。
默认不检查 testWhileIdle: false, timeBetweenEvictionRunsMillis: -1

不足：
1. 达到 maxTotal之后，签出将阻塞当前线程；无法配置阻塞时间；
如果调用层没有配置好，则一条链路都卡死。
2. 不支持底层connection超时配置，依赖OS的时间（一般10分钟）。
10分钟太长，也可能造成链路卡死。

### Druid
Druid是阿里巴巴团队贡献的一个数据库连接池实现。
特点：
1. 支持大部分 BasicDataSource的配置属性，包括 maxTotal(maxActive):8,
maxIdle:8, initialSize:0, minIdle:0,validationQuery:null, testOnBorrow:true,
testWhileIdle:false,timeBetweenEvictionRunsMillis:60s，validationQueryTimeout：-1
2. 支持 maxWait（默认-1） 获取连接时最大等待时间。

不足：
1. 官方的文档上，没有出现validationQueryTimeout配置，虽然底层支持。
2. 与 BasicDataSource 一样，不支持底层 connection的超时配置。





其他：
1. Druid通过filter-chain的方式支持了一些额外的功能，如Sql运行监控StatFilter，可以配置servlet在网页上查看。
由于StatFilter使用了自己实现的SQLParser，能提供更详细的运行信息。



end。
