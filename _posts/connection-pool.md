---
title: Druid、BasicDataSource连接池配置参考
date: 2016-03-05 07:07:14
tags:
 - 连接池
---

连接池的出现，是由于建立数据库连接花费较大，包括TCP三次握手、连接初始化、DB端资源准备等；
而且系统要控制连接的数量，防止资源耗尽。

考虑一些异常场景：
E1. 高并发，即达到 maxTotal；签出连接是否阻塞，是否支持超时
E2. 数据库重启；原连接失效，在idle状态、或签出时，能否检测并处理
E3. client和DB之间，有防火墙，且防火墙设置了tcp的最长空闲时间；
原连接失效，且client和DB都不知道。
E4. 网络延迟，建立tcp和数据传输耗时严重；超时配置，是否支持底层连接池超时配置


### Druid 配置解读

[Druid官方配置参考](https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE)


{% codeblock lang:xml %}

<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destroy-method="close">
     <property name="url" value="com.mysql.jdbc.Driver" />
     <property name="username"><value>${jdbc_user}</value></property>
     <property name="password" value="${jdbc_password}" />

     <property name="initialSize"><value>1</value></property>
     <property name="maxActive"><value>20</value></property>
     <property name="maxIdle"><value>20</value></property>
     <property name="minIdle"><value>1</value></property>

     <property name="maxWait"><value>10000</value></property>
     <property name="useUnfairLock"><value>true</value></property>

     <property name="validationQuery"><value>SELECT 'x'</value></property>
     <property name="validationQueryTimeout"><value>10</value></property>

     <property name="timeBetweenEvictionRunsMillis"><value>60000</value></property>
     <property name="minEvictableIdleTimeMillis"><value>300000</value></property>

     <property name="testWhileIdle"><value>true</value></property>
     <property name="testOnBorrow"><value>false</value></property>
     <property name="testOnReturn"><value>false</value></property>

 </bean>
{% endcodeblock %}

上面的配置，针对mysql做了调整。说明：
1. 去掉了 filters:stat 的配置。druid在sql监控上做了很多工作，比如提供自己实现的 sqlparser 解析，
来提供更精细化的数据，还可以配置 servlet 展示页面，具体参考官网。这里假设项目已有其他方式监控sql运行状态。
2. maxWait: 60000 -> 10000，正常情况下，主要是创建连接的时间；
在高并发的场景下，连接数达到maxActive，主要是资源竞争线程被锁住的时间。这个配置，处理了E1异常。
比如Dubbo服务超时为3s（服务的实现调用了jdbc），这里配置过大没有意义。这里改成10秒。
3. 增加 useUnfairLock: true，默认是false，公平锁带来很大的性能问题；
0.2.8版本之后，建议使用非公平锁，兼顾公平和性能。
4. timeBetweenEvictionRunsMillis:60s， Druid检查连接是否要删除的间隔，
minEvictableIdleTimeMillis：5min 一个连接至少必须存活多长时间才被驱逐。这两个参数配合使用，
理论上，连接最大的存活时间是  minEvictableIdleTimeMillis + timeBetweenEvictionRunsMillis
5. 增加 validationQueryTimeout:10s，注意单位是秒。这里的实现是直接调用 jdbc Statement.setQueryTimeout(int seconds)
方法。
6. testWhileIdle 这个很重要，如果 minIdle > 0，那这些idle的连接，就需要和DB保持一个心跳，防止上文提到的E2 E3异常。
7. 去掉了poolPreparedStatements这个配置，mysql建议关闭 PreparedStatements 缓存。


其他：
1. Druid 默认开启了 exceptionSorter，根据不同的db做了异常处理优化，
假如发现是致命不可恢复的error code，则直接删除连接，避免祸害后续使用。

### DBCP

[commons-dbcp2 配置参考](https://commons.apache.org/proper/commons-dbcp/configuration.html)

<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="com.mysql.jdbc.Driver" />
    <property name="url" value="jdbc:mysql://localhost:3306/test" />
    <property name="username" value="username" />
    <property name="password" value="password" />

    <property name="initialSize" value="1" />
    <property name="maxTotal" value="20" />
    <property name="maxIdle" value="20" />
    <property name="minIdle" value="1" />

    <property name="maxWaitMillis" value="10000" />


    <property name="validationQuery" value="SELECT 1;" />
    <property name="validationQueryTimeout" value="10" />

    <property name="timeBetweenEvictionRunsMillis" value="60000" />
    <property name="minEvictableIdleTimeMillis" value="300000" />

    <property name="testWhileIdle" value="true" />
    <property name="testOnBorrow"><value>false</value></property>
    <property name="testOnReturn"><value>false</value></property>

</bean>

以上配置，由官网说明整理而来：
1. maxTotal 原来的属性叫 maxActive(就像Druid抄袭的那样)，dbcp2改成maxTotal了。
2. maxWaitMillis 原来叫 maxWait(Druid复制过来了)，含义却有所不同。DBCP2底层使用
commons-pool2 对象池实现，这个属性直接设置到了 GenericObjectPool 的maxWaitMillis属性上，
只在确认maxTotal达到、且所有资源都签出时，才会起作用。

end。
