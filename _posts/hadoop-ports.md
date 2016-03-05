---
title: hadoop 端口解读
date: 2016-03-01 17:12:14
tags:
 - hadoop
---

### NameNode
8020或9000
> * NameNode RPC端口，为client提供元数据服务等。
涉及：NamenodeProtocols将很多接口合在一起，包括 ClientProtocol,DatanodeProtocol（和datanode交互）等

50070
> * NameNode对外暴露的http端口
* 通过浏览器查看NameNode状态，datanode列表，浏览hdfs文件系统等

### Datanode
50010
>Datanode RPC数据库传输接口，dn的数据块通过这个端口进出。涉及：hdfs.protocol.ClientProtocol

50020
>Datanode元数据操作端口，比如namenode可以强制datanode立即汇报block信息，以及升级时发shutdown消息给datanode。涉及：ClientDatanodeProtocol


### ResourceManager
8030
>调度器端口，ApplicationMaster通过该地址向RM申请资源、释放资源等。涉及：ApplicationMasterProtocol

8031
> ResourceManager 对NodeManager暴露的地址。NodeManager通过该地址向RM汇报心跳，领取任务等。
涉及：ResourceTracker

8032
>ResourceManager 对yarn客户端暴露的地址。客户端通过该地址向RM提交应用程序，获取应用状态以及杀死应用程序等。涉及：ApplicationClientProtocol

8033
>RM管理端口 ResourceManager 对管理员暴露的访问地址。管理员通过该地址向RM发送管理命令等。涉及：ResourceManagerAdministrationProtocol

8088
>webui ResourceManager对外http端口。用户可在浏览器中查看yarn任务的状态、队列、任务节点信息等。

### NodeManager
8040  
> RPC端口，用于实现资源本地化。比如mapreduce任务节点必须下载jar包到本地执行。

0(随机可用端口）
> NodeManager的容器管理端口，主要用于 ApplicationMaster和NodeManager交互，启动、停止分配到的容器。涉及： ContainerManagementProtocol


8042
>NodeManager 对外暴露的http端口。
