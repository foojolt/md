---
title: Yarn 理解
date: 2016-03-02 17:20:14
tags:
 - hadoop
 - yarn
---

Yarn (Yet another resource negotiator )称为 MRv2，主要改进是：
1. 将原 jobTracker 的功能拆分成：资源管理（ResourceManager进程），具体的任务执行、失败重连等（Application Master进程）。
2. 做成通用的集群计算资源管理器，可以支持MR之外的计算框架，如Spark

### 主要数据流

![yarn_architecture](../images/yarn_architecture.gif)

ResourceManager 由两个组件：
1. Scheduler 调度器，结合集群资源的状态、以及任务的需求，分配container。比如常见的 CapacityScheduler 支持树形结构的队列，每个队列可以配置ACL。
2. ApplicationsManager 任务管理器，它负责处理Job提交，启动、监控和重启任务的ApplicationMaster

NodeManager 在任务节点上部署，负责启动本节点的容器、向RM/ResourceTracker汇报状态。

### 任务执行过程
![Yarn Job](../images/yarn-flow.png)
1. 客户端启动一个job： 配置属性，比如MR的mapper/reducer类，输入文件输出文件等，
