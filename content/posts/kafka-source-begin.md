---
title: "Kafka源码阅读环境搭建"
date: 2018-11-07
draft: false
categories: ["Kafka"]
tags: ["Kafka", "Scala"]
---


记录Kafka源码阅读环境的搭建过程。

## 序

在大数据系统中Kafka应用广泛，借助源码阅读可以加深对组件的理解，同时可以拾起Scala语言。

## 安装依赖软件

* JDK
* Scala
* Gradle

## 构建IDEA工程

在源码目录下运行 gradle idea。

遇到的问题：

```java
* What went wrong:  
A problem occurred evaluating root project 'kafka-0.10.0.1-src'.  
> Failed to apply plugin [class 'org.gradle.api.plugins.scala.ScalaBasePlugin']  
   > No such property: useAnt for class: org.gradle.api.tasks.scala.ScalaCompileOptions  
```

需要在build.gradle开头加入：

```
ScalaCompileOptions.metaClass.daemonServer = true  
ScalaCompileOptions.metaClass.fork = true  
ScalaCompileOptions.metaClass.useAnt = false  
ScalaCompileOptions.metaClass.useCompileDaemon = false 
```

然后构建完成。

![构建过程](/images/kafka-source-begin-1.jpg)


## 打开工程

然后用IDEA打开工程，kafka server的启动类是 `kafka.Kafka`，启动时需要指定配置文件 `config/server.properties`。

这里我修改了日志路径和ZK的地址。
```
log.dirs=D:\\dev\\kafka-logs
zookeeper.connect=ubuntu:2181
```

配置启动选项，指定server.properties配置文件。

![配置启动项](/images/kafka-source-begin-2.jpg)

运行后可以看到kafka成功启动的日志：

```java
[2018-11-07 14:17:20,673] INFO Initiating client connection, connectString=ubuntu:2181 sessionTimeout=6000 watcher=org.I0Itec.zkclient.ZkClient@6a79c292 (org.apache.zookeeper.ZooKeeper)
[2018-11-07 14:17:21,029] INFO Waiting for keeper state SyncConnected (org.I0Itec.zkclient.ZkClient)
[2018-11-07 14:17:21,032] INFO Opening socket connection to server ubuntu/10.240.209.160:2181. Will not attempt to authenticate using SASL (unknown error) (org.apache.zookeeper.ClientCnxn)
[2018-11-07 14:17:21,039] INFO Socket connection established to ubuntu/10.240.209.160:2181, initiating session (org.apache.zookeeper.ClientCnxn)
[2018-11-07 14:17:21,051] INFO Session establishment complete on server ubuntu/10.240.209.160:2181, sessionid = 0x100000ae61d005b, negotiated timeout = 6000 (org.apache.zookeeper.ClientCnxn)
[2018-11-07 14:17:21,054] INFO zookeeper state changed (SyncConnected) (org.I0Itec.zkclient.ZkClient)
[2018-11-07 14:17:21,318] INFO Cluster ID = W3aGwjIPScGmQWjSVjuapQ (kafka.server.KafkaServer)
[2018-11-07 14:17:21,357] INFO Log directory 'D:\dev\kafka-logs' not found, creating it. (kafka.log.LogManager)
[2018-11-07 14:17:21,367] INFO Loading logs. (kafka.log.LogManager)
[2018-11-07 14:17:21,377] INFO Logs loading complete in 10 ms. (kafka.log.LogManager)
[2018-11-07 14:17:21,441] INFO Starting log cleanup with a period of 300000 ms. (kafka.log.LogManager)
[2018-11-07 14:17:21,444] INFO Starting log flusher with a default period of 9223372036854775807 ms. (kafka.log.LogManager)
[2018-11-07 14:17:21,449] WARN No meta.properties file under dir D:\dev\kafka-logs\meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2018-11-07 14:17:21,498] INFO Awaiting socket connections on 0.0.0.0:9092. (kafka.network.Acceptor)
[2018-11-07 14:17:21,501] INFO [Socket Server on Broker 0], Started 1 acceptor threads (kafka.network.SocketServer)
[2018-11-07 14:17:21,525] INFO [ExpirationReaper-0], Starting  (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2018-11-07 14:17:21,526] INFO [ExpirationReaper-0], Starting  (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2018-11-07 14:17:21,563] INFO Creating /controller (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2018-11-07 14:17:21,579] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2018-11-07 14:17:21,581] INFO 0 successfully elected as leader (kafka.server.ZookeeperLeaderElector)
[2018-11-07 14:17:21,683] INFO [ExpirationReaper-0], Starting  (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2018-11-07 14:17:21,686] INFO [ExpirationReaper-0], Starting  (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2018-11-07 14:17:21,687] INFO [ExpirationReaper-0], Starting  (kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2018-11-07 14:17:21,699] INFO [GroupCoordinator 0]: Starting up. (kafka.coordinator.GroupCoordinator)
[2018-11-07 14:17:21,706] INFO [GroupCoordinator 0]: Startup complete. (kafka.coordinator.GroupCoordinator)
[2018-11-07 14:17:21,707] INFO [Group Metadata Manager on Broker 0]: Removed 0 expired offsets in 2 milliseconds. (kafka.coordinator.GroupMetadataManager)
[2018-11-07 14:17:21,741] INFO Will not load MX4J, mx4j-tools.jar is not in the classpath (kafka.utils.Mx4jLoader$)
[2018-11-07 14:17:21,766] INFO New leader is 0 (kafka.server.ZookeeperLeaderElector$LeaderChangeListener)
[2018-11-07 14:17:21,790] INFO Creating /brokers/ids/0 (is it secure? false) (kafka.utils.ZKCheckedEphemeral)
[2018-11-07 14:17:21,799] INFO Result of znode creation is: OK (kafka.utils.ZKCheckedEphemeral)
[2018-11-07 14:17:21,803] INFO Registered broker 0 at path /brokers/ids/0 with addresses: PLAINTEXT -> EndPoint(HIH-L-5338.cn.net.ntes,9092,PLAINTEXT) (kafka.utils.ZkUtils)
[2018-11-07 14:17:21,804] WARN No meta.properties file under dir D:\dev\kafka-logs\meta.properties (kafka.server.BrokerMetadataCheckpoint)
[2018-11-07 14:17:21,826] WARN Error while loading kafka-version.properties :null (org.apache.kafka.common.utils.AppInfoParser)
[2018-11-07 14:17:21,827] INFO Kafka version : unknown (org.apache.kafka.common.utils.AppInfoParser)
[2018-11-07 14:17:21,827] INFO Kafka commitId : unknown (org.apache.kafka.common.utils.AppInfoParser)
[2018-11-07 14:17:21,829] INFO [Kafka Server 0], started (kafka.server.KafkaServer)
```

## 验证

然后用kafka二进制包（注意是下载的二进制包，而不是源码包）中自带的脚本收发消息进行验证。

```
 D:\GitHub\kafka\bin\windows> .\kafka-topics.bat --create --zookeeper ubuntu:2181 --replication-factor 1 --partitions 1 --topic test
错误: 找不到或无法加载主类 C:\ProgramFiles\Java\jdk1.8.0_181\lib\dt.jar;
```

修改kafka-run-class.bat中的：
```bash
set COMMAND=%JAVA% %KAFKA_HEAP_OPTS% %KAFKA_JVM_PERFORMANCE_OPTS% %KAFKA_JMX_OPTS% %KAFKA_LOG4J_OPTS% -cp %CLASSPATH% %KAFKA_OPTS% %*
```
为：
```bash
set COMMAND=%JAVA% %KAFKA_HEAP_OPTS% %KAFKA_JVM_PERFORMANCE_OPTS% %KAFKA_JMX_OPTS% %KAFKA_LOG4J_OPTS% -cp "%CLASSPATH%" %KAFKA_OPTS% %*
```

![消息收发](/images/kafka-source-begin-3.jpg)

就此Kafka源码阅读环境搭建完成。


