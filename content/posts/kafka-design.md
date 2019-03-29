---
title: "Kafka的设计"
date: 2016-11-27
draft: false
categories: ["Kafka"]
tags: [ "Kafka"]
---

![哲学思想](/images/kafka-design-1.jpg)

本文是阅读Kafka文档的一点笔记。

## 概要

定义❓ 消息队列源于IPC，Unix中的IPC模型如下：

![IPC模型](/images/kafka-design-2.png)


消息队列的特点❓

* IPC
* 解耦，异步处理
* 发布/订阅模式

分布式环境❓

* 消息中间件
* 容错，可扩展性
* ActiveMQ, Kafka, RabbitMQ, ZeroMQ, RocketMQ


## Kafka的设计

☐ distributed, real-time processing

☐ partitioning

☐ producer/consumer group

☐ pagecache-centric

## 持久化

* 磁盘并没有想象中的那么慢，特别是顺序写的时候（OS优化、预取、批量写）。

|顺序写      |   随机写|
|---|---|
|600MB/sec  |  100k/sec|

* 索引结构采用消费队列（而不是BTree）

## 高效

大量小的IO操作？ 批量操作（larger network packets, larger sequential disk operations, contiguous memory blocks）均摊网络通信的开销。

大量字节拷贝？ 使用零拷贝技术，如Linux下的sendfile系统调用。

## Broker

* 存储
* 多副本
* 日志清理

## Producer

* Load balancing（random, hash func）
* Asynchronous send（latency vs throughput）


## Consumer
* pull
* consumer position

![组件交互](/images/kafka-design-3.jpg)