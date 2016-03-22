---
title: Spark essentials
date: 2016-03-14 11:07:14
tags:
 - spark
---

### 基础

RDD组成：
1. 分区列表
2. 分区计算函数
3. 父RDD依赖列表
4. 可选： key,value RDD的Partition函数
5. 可选： hdfs rdd的优选位置（preferred location）

./bin/spark-shell  --master local[3]
val r = sc.parallelize( Array( (1,2), (2,3), (3,4), (3,5)  ), 4 )
r.toDebugString


### RDD API 

计算split：
abstract def
compute(split: Partition, context: TaskContext): Iterator[T]

Union组合RDD：
++(other: RDD[T]): RDD[T]

值聚合：
def
aggregate[U](zeroValue: U)(seqOp: (U, T) ⇒ U, combOp: (U, U) ⇒ U)(implicit arg0: ClassTag[U]): U
r.aggregate( "" )( ( t, a ) => t + a._1.toString, ( x, y ) => x + y  )

groupByKey有内存警告



### Job运行原理

Transformation 只是构造DAG，不做其他事情。通过sc.runJob 物化
执行优化：
1. transformation 可以 pipeline
2. graph可能由于cache/checkpoint被截断，之前的不用计算了

Job is list of stages
    stage is list of tasks ( stage内的task彼此无依赖 )

shuffle happens between stages

Job优化：
1. 减少 shuffle: 比如用reduceByKey而不是 groupByKey
2. 早点调用filter
3. 并发度控制： 太多调度不过来（同时运行的task有限）；太少就类似单机了
4. 选择序列化器： 比如 kryo, 用在 cache 和 shuffle
5. 选择cache级别： memory_only，用原生的jvm序列化；memory_only_ser 可以减少内存使用； memory_and_disk 容错性增强，减少重复计算
6. 采用lzf压缩，提高性能
7. 启用 speculative 执行预防stragglers: 有的任务运行慢，可以开启探测，重新调度；可以配置探测间隔；乘数（大于乘数＊中位数的任务，将重新跑）；完成的任务数比例，确保在大部分任务跑完时才探测

rdd.toDebugString 查看DAG


### 压缩

压缩：用CPU换IO
mapreduce压缩可用在三个阶段：
1. 输入文件
2. map输出
3. reduce输出

算法：
lzo  支持分片，压缩速度快；但压缩比低(snapy/lzf 和 lzo 类似)
bzip2 支持分片，压缩比高；但压缩慢

### Shuffle

shuffle中间文件的问题：
个数是 t * R ： 每个 executor 最多 t个task同时运行(一般等于core_num)

shuffle默认启用sort，之前的版本有hash版本的，因为spark认为sort带来额外开销。但hash需要放内存中；sort是外部排序

默认采用netty传输数据。

http://jerryshao.me/architecture/2014/01/04/spark-shuffle-detail-investigation/

### Akka RPC





