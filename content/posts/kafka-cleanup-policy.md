---
title: "Kafka中的2种日志清理策略"
date: 2018-09-14
draft: false
categories: ["Kafka"]
tags: ["Kafka"]
---

初体验Kafka中的两种日志清理策略：log compaction和delete。

## 序

Kafka是一个基于日志的流处理平台，一个topic可以有多个分区（partition），分区是复制的基本单元，在单节点上，一个分区的数据文件可以存储在多个磁盘目录中，配置项是：


```
# A comma separated list of directories under which to store log files
log.dirs=/home/storm/dev/kafka-logs
```

每个分区的日志文件存储的时候又会分成一个个的segment，默认日志段（segment）的大小是1GB，segment是日志清理的基本单元，当前正在使用的segment是不会被清理的。

```
# The maximum size of a log segment file. When this size is reached a new log segment will be created.
log.segment.bytes=1073741824
```


## 日志清理

Kafka Broker 的日志清理功能在配置 `log.cleaner.enable=true` 后会开启一些清理线程，执行定时清理任务。在kafka 0.9.0之后 log.cleaner.enable 默认是true。 支持的清理策略（`log.cleanup.policy`）有2种：delete和compact，默认是delete。




## compact 清理策略（log compaction）


log compaction 实现的是一个topic的一个分区中，只保留最近的某个key对应的value，如果要删除某个消息可以发送一个墓碑消息（tomestone）：(key, null)。为了展示这个过程，修改 Broker 的配置：把segment的大小调小点，清理策略改为 compact。

```
# 25KB
log.segment.bytes=25600 
log.cleanup.policy=compact
```


批量发送一些带有key的消息。


```bash
➜  test-0 ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test --property "parse.key=true" --property "key.separator=:" < msg.txt
```

然后可以在日志目录中看到日志文件的结构。

```bash
➜  kafka-logs cd test-0 
➜  test-0 ls -alh
total 160K
drwxrwxr-x  2 storm storm 4.0K Sep 11 18:47 .
drwxrwxr-x 53 storm storm 4.0K Sep 11 18:47 ..
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000000.index
-rw-rw-r--  1 storm storm   78 Sep 11 17:27 00000000000000000000.log
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000000.timeindex
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000153.index
-rw-rw-r--  1 storm storm  175 Sep 11 17:27 00000000000000000153.log
-rw-rw-r--  1 storm storm   10 Sep 11 17:27 00000000000000000153.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000153.timeindex
-rw-rw-r--  1 storm storm    8 Sep 11 18:47 00000000000000000296.index
-rw-rw-r--  1 storm storm  25K Sep 11 17:27 00000000000000000296.log
-rw-rw-r--  1 storm storm   10 Sep 11 17:27 00000000000000000296.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000296.timeindex
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.index
-rw-rw-r--  1 storm storm  16K Sep 11 18:47 00000000000000000522.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000522.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000522.timeindex
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000665.index
-rw-rw-r--  1 storm storm  16K Sep 11 18:47 00000000000000000665.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000665.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000665.timeindex
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.index
-rw-rw-r--  1 storm storm  25K Sep 11 18:47 00000000000000000808.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000808.snapshot
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.timeindex
-rw-rw-r--  1 storm storm    8 Sep 11 10:44 leader-epoch-checkpoint

➜  test-0 ls -alh
total 164K
drwxrwxr-x  2 storm storm 4.0K Sep 11 18:48 .
drwxrwxr-x 53 storm storm 4.0K Sep 11 18:48 ..
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000000.index
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000000.index.deleted
-rw-rw-r--  1 storm storm   73 Sep 11 17:27 00000000000000000000.log
-rw-rw-r--  1 storm storm   78 Sep 11 17:27 00000000000000000000.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000000.timeindex
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000000.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000153.index.deleted
-rw-rw-r--  1 storm storm  175 Sep 11 17:27 00000000000000000153.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000153.timeindex.deleted
-rw-rw-r--  1 storm storm    8 Sep 11 18:47 00000000000000000296.index.deleted
-rw-rw-r--  1 storm storm  25K Sep 11 17:27 00000000000000000296.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000296.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.index
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.index.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.log
-rw-rw-r--  1 storm storm  16K Sep 11 18:47 00000000000000000522.log.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.timeindex
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000522.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000665.index
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000665.index.deleted
-rw-rw-r--  1 storm storm  175 Sep 11 18:47 00000000000000000665.log
-rw-rw-r--  1 storm storm  16K Sep 11 18:47 00000000000000000665.log.deleted
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000665.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000665.timeindex
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000665.timeindex.deleted
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.index
-rw-rw-r--  1 storm storm  25K Sep 11 18:47 00000000000000000808.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000808.snapshot
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.timeindex
-rw-rw-r--  1 storm storm    8 Sep 11 10:44 leader-epoch-checkpoint
```


可以看到除了当前segment之外，前面的segments都已经得到了清理/压缩，从偏移量（offset）出现缺失可到看出来。


```bash
➜  kafka_2.11-2.0.0 ./bin/kafka-run-class.sh kafka.tools.DumpLogSegments  --deep-iteration --files /home/storm/dev/kafka-logs/test-0/00000000000000000000.log 
Dumping /home/storm/dev/kafka-logs/test-0/00000000000000000000.log
Starting offset: 0
offset: 521 position: 0 CreateTime: 1536658031117 isvalid: true keysize: 4 valuesize: 0 magic: 2 compresscodec: NONE producerId: -1 producerEpoch: -1 sequence: -1 isTransactional: false headerKeys: []
➜  kafka_2.11-2.0.0 ./bin/kafka-run-class.sh kafka.tools.DumpLogSegments  --deep-iteration --files /home/storm/dev/kafka-logs/test-0/00000000000000000665.log 
Dumping /home/storm/dev/kafka-logs/test-0/00000000000000000665.log
Starting offset: 665
offset: 807 position: 0 CreateTime: 1536662844868 isvalid: true keysize: 4 valuesize: 100 magic: 2 compresscodec: NONE producerId: -1 producerEpoch: -1 sequence: -1 isTransactional: false headerKeys: []
```

标记为deleted的segments会在1天后被清除。

```bash
➜  test-0 pwd
/home/storm/dev/kafka-logs/test-0
➜  test-0 date    
Wed Sep 12 09:48:45 CST 2018
➜  test-0 ls -alh 
total 72K
drwxrwxr-x  2 storm storm 4.0K Sep 11 18:48 .
drwxrwxr-x 53 storm storm 4.0K Sep 11 19:51 ..
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000000.index
-rw-rw-r--  1 storm storm   73 Sep 11 17:27 00000000000000000000.log
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000000.timeindex
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.index
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.log
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.timeindex
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000665.index
-rw-rw-r--  1 storm storm  175 Sep 11 18:47 00000000000000000665.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000665.snapshot
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000665.timeindex
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.index
-rw-rw-r--  1 storm storm  25K Sep 11 18:47 00000000000000000808.log
-rw-rw-r--  1 storm storm   10 Sep 11 18:47 00000000000000000808.snapshot
-rw-rw-r--  1 storm storm  10M Sep 11 18:47 00000000000000000808.timeindex
-rw-rw-r--  1 storm storm    8 Sep 11 10:44 leader-epoch-checkpoint
```

## delete 清理策略（默认）

再来看看 delete 清理策略，这种策略就是我们默认看到的数据保留特点，超过特定的数据量或者时间，日志就会被删除，这里涉及的 Broker 配置参数是：`log.retention.bytes` 和 `log.retention.hours`（等价于 `log.retention.minutes`，`log.retention.ms`）默认值为：

```
# 需要自己根据实际情况设置
log.retention.bytes=-1

# 默认的保留时间是7天
log.retention.hours=168 
```

为了能看出日志删除的效果，这里把保留时间调小，设置为60分钟，然后可以看到，除了当前正在使用的segment，前面的segments都被删除了（标记为deleted，1天后会物理删除）。


```
# The minimum age of a log file to be eligible for deletion due to age
log.retention.minutes=60
```


```bash
➜  kafka-logs ls -alh test-0
total 220K
drwxrwxr-x  2 storm storm 4.0K Sep 13 11:12 .
drwxrwxr-x 53 storm storm 4.0K Sep 13 11:12 ..
-rw-rw-r--  1 storm storm    0 Sep 11 17:27 00000000000000000000.index.deleted
-rw-rw-r--  1 storm storm   73 Sep 11 17:27 00000000000000000000.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 11 17:27 00000000000000000000.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.index.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.log.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000522.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 11 18:47 00000000000000000665.index.deleted
-rw-rw-r--  1 storm storm  175 Sep 11 18:47 00000000000000000665.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 11 18:47 00000000000000000665.timeindex.deleted
-rw-rw-r--  1 storm storm    8 Sep 12 10:50 00000000000000000808.index.deleted
-rw-rw-r--  1 storm storm  25K Sep 11 18:47 00000000000000000808.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:50 00000000000000000808.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 12 10:50 00000000000000001034.index.deleted
-rw-rw-r--  1 storm storm  16K Sep 12 10:50 00000000000000001034.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:50 00000000000000001034.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 12 10:50 00000000000000001177.index.deleted
-rw-rw-r--  1 storm storm  16K Sep 12 10:50 00000000000000001177.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:50 00000000000000001177.timeindex.deleted
-rw-rw-r--  1 storm storm    8 Sep 12 10:51 00000000000000001320.index.deleted
-rw-rw-r--  1 storm storm  25K Sep 12 10:50 00000000000000001320.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:51 00000000000000001320.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 12 10:51 00000000000000001546.index.deleted
-rw-rw-r--  1 storm storm  16K Sep 12 10:51 00000000000000001546.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:51 00000000000000001546.timeindex.deleted
-rw-rw-r--  1 storm storm    0 Sep 12 10:51 00000000000000001689.index.deleted
-rw-rw-r--  1 storm storm  16K Sep 12 10:51 00000000000000001689.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 12 10:51 00000000000000001689.timeindex.deleted
-rw-rw-r--  1 storm storm    8 Sep 13 11:12 00000000000000001832.index.deleted
-rw-rw-r--  1 storm storm  25K Sep 12 10:51 00000000000000001832.log.deleted
-rw-rw-r--  1 storm storm   12 Sep 13 11:12 00000000000000001832.timeindex.deleted
-rw-rw-r--  1 storm storm  10M Sep 13 11:12 00000000000000002058.index
-rw-rw-r--  1 storm storm    0 Sep 13 11:12 00000000000000002058.log
-rw-rw-r--  1 storm storm   10 Sep 13 11:08 00000000000000002058.snapshot
-rw-rw-r--  1 storm storm  10M Sep 13 11:12 00000000000000002058.timeindex
-rw-rw-r--  1 storm storm   11 Sep 13 11:12 leader-epoch-checkpoint

➜  kafka-logs date
Fri Sep 14 09:19:41 CST 2018
➜  kafka-logs ls -alh test-0              
total 16K
drwxrwxr-x  2 storm storm 4.0K Sep 13 11:13 .
drwxrwxr-x 53 storm storm 4.0K Sep 14 09:19 ..
-rw-rw-r--  1 storm storm  10M Sep 13 11:12 00000000000000002058.index
-rw-rw-r--  1 storm storm    0 Sep 13 11:12 00000000000000002058.log
-rw-rw-r--  1 storm storm   10 Sep 13 11:08 00000000000000002058.snapshot
-rw-rw-r--  1 storm storm  10M Sep 13 11:12 00000000000000002058.timeindex
-rw-rw-r--  1 storm storm   11 Sep 13 11:12 leader-epoch-checkpoint
```


## 参考

[Kafka Architecture: Log Compaction](http://cloudurable.com/blog/kafka-architecture-log-compaction/index.html)

[4.8 Log Compaction](https://kafka.apache.org/documentation/#compaction)