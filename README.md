[主页](https://github.com/vonzhou/Blog)  | [读书](https://github.com/vonzhou/readings)  | [知乎](https://www.zhihu.com/people/vonzhou) 
---
# 编程之路 - Build Your Programming Culture

## 订阅

点击 [Blog](https://github.com/vonzhou/Blog) 页面右上角的 `Watch` ->  `Watching` 订阅本博客，这样本博客的更新后你会收到通知。



## Java

* [JVM GC 总结](https://github.com/vonzhou/learning-java/blob/master/src/javavirtualmachine/gc/GC.md) 2019.2.21
* [为什么枚举是实现单例最好的方式？](https://github.com/vonzhou/learning-java/blob/master/src/lang/enumsingleton/Enum.md)  2019.2.14
* [从连接池(JedisPool)获取Redis连接源码分析](https://github.com/vonzhou/learning-java/tree/master/src/framework/redis/jedispoolget) 2018.12.14
* [Redis中键的过期删除策略](https://github.com/vonzhou/learning-java/blob/master/src/framework/redis/redisexpire/) 2018.9.9
* [如何保证ArrayList在多线程环境下的线程安全性](https://github.com/vonzhou/learning-java/tree/master/src/collection/arraylistthreadsafe2) 2018.9.7
* [记一次 ArrayList 线程安全问题](https://github.com/vonzhou/learning-java/tree/master/src/collection/arraylistthreadsafe) 2018.7.12
* [Java字节码工具AsmTools介绍](https://github.com/vonzhou/learning-java/tree/master/src/framework/asmtools) 2018.11.27
* [CAS 的底层实现](https://github.com/vonzhou/learning-java/tree/master/src/concurrent/cas) 2018.9.19
* [Disruptor中的事件消费模式](https://github.com/vonzhou/learning-java/tree/master/src/framework/disruptor)  2018.9.28
* [Disruptor 快速入门](https://github.com/vonzhou/learning-java/blob/master/src/framework/disruptor/DisruptorHello.md)  2018.9.21
* [ArrayBlockingQueue与Disruptor的性能对比](https://github.com/vonzhou/learning-java/tree/master/src/framework/disruptor/threadpoolvsdisruptor)   2018.12.1
* [IntegerCache源码阅读](https://github.com/vonzhou/learning-java/blob/master/src/lang/IntegerCache.md) 2018.12.19
* [深入理解条件变量Condition](https://github.com/vonzhou/learning-java/blob/master/src/concurrent/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E6%9D%A1%E4%BB%B6%E5%8F%98%E9%87%8FCondition.md) 2018.11.11
* [Hashtable 和 HashMap 的对比](https://github.com/vonzhou/learning-java/blob/master/src/collection/HashtableVsHashMap.md)


### JDK源码阅读

* [ThreadLocal](https://github.com/vonzhou/learning-java/blob/master/src/lang/ThreadLocal.md)
* [ArrayList](https://github.com/vonzhou/learning-java/blob/master/src/collection/ArrayList.md)
* [Collections](https://github.com/vonzhou/learning-java/blob/master/src/collection/Collections.md)
* [ConcurrentHashMap](https://github.com/vonzhou/learning-java/blob/master/src/collection/ConcurrentHashMap.md)
* [可重入锁 ReentrantLock](https://github.com/vonzhou/learning-java/blob/master/src/concurrent/ReentrantLock.md)  
* [条件变量 Condition/ConditionObject](https://github.com/vonzhou/learning-java/blob/master/src/concurrent/%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E6%9D%A1%E4%BB%B6%E5%8F%98%E9%87%8FCondition.md#condition-%E5%AE%9E%E7%8E%B0%E5%88%86%E6%9E%90)


## Kafka

* [大面积offset commit失败，导致不停Rebalance，大量消息重复消费的问题](https://github.com/vonzhou/learning-java/blob/master/src/framework/kafka/rebalancejitter/README.md) 2019.1.30
* [Kafka源码阅读环境搭建](https://github.com/vonzhou/Blog/blob/master/Contents/BigData/kafka-source-begin.md)  2018.11.7
* [Kafka中的2种日志清理策略](https://github.com/vonzhou/Blog/blob/master/Contents/BigData/kafka-cleanup-policy.md) 2018.914


## Spring/SpringBoot/SpringCloud

* [BeanUtils.copyProperties 源码分析](https://github.com/vonzhou/learning-spring/tree/master/src/main/java/com/vonzhou/learningspring/copyproperties) 2019.2.27
* [解决Zuul无法同时转发Multipart和JSON请求的问题](https://github.com/vonzhou/Blog/blob/master/Contents/Spring/zuul-forward-multipart-and-json.md)  2018.10.10
* [如何加快 Spring Boot 项目的启动速度？](https://github.com/vonzhou/Blog/blob/master/Contents/Spring/spring-boot-speedup.md) 2018.9.4
* [Spring Boot 执行初始化逻辑的方法](https://github.com/vonzhou/spring-boot-examples/tree/master/spring-boot-init-method)  2018.9.18
* [Spring源码阅读 - bean实例化浅析](https://github.com/vonzhou/learning-spring/blob/master/sourcereading/bean%E5%AE%9E%E4%BE%8B%E5%8C%96%E6%B5%85%E6%9E%90.md) 2016.9.2
* [Spring源码阅读 - bean解析初体验](https://github.com/vonzhou/learning-spring/blob/master/sourcereading/bean%E8%A7%A3%E6%9E%90%E5%88%9D%E4%BD%93%E9%AA%8C.md)  2016.9.1


## BigData 大数据

* [《HBase权威指南》读书笔记](https://github.com/vonzhou/Blog/blob/master/Contents/BigData/hbase-definitive.md) 2018.12.20
* [运行《HBase权威指南》书中代码](https://github.com/vonzhou/hbase-book#%E8%BF%90%E8%A1%8Chbase%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97%E4%B9%A6%E4%B8%AD%E4%BB%A3%E7%A0%81) 2018.12.18

## Nginx

* [Nginx后端响应不完整问题分析](https://github.com/vonzhou/Blog/blob/master/Contents/Nginx/nginx-temp-file.md)  2019.1.4

## Linux

* [curl URL是否加单引号引发的问题](https://github.com/vonzhou/Blog/blob/master/Contents/Linux/curl/singlequote/curl-single-quote.md) 2018.12.7
* [Linux常用命令总结](https://github.com/vonzhou/Blog/blob/master/Contents/Linux/linux-commands.md)   2018.8.31
* [netstat 命令](https://github.com/vonzhou/Blog/tree/master/Contents/Linux/netstat)  2017.5.16
* [tcpdump 命令](https://github.com/vonzhou/Blog/tree/master/Contents/Linux/tcpdump)  2017.5.16
* [《深入理解计算机系统结构》实战](https://github.com/vonzhou/CSAPP)   2015.3.24


## Scala

* [《快学Scala》读书笔记](https://github.com/vonzhou/ScalaImpatient#%E5%BF%AB%E5%AD%A6scala%E8%AF%BB%E4%B9%A6%E7%AC%94%E8%AE%B0)  2018.12.31


## Database 数据库

* [SQL优化方法总结](https://github.com/vonzhou/Blog/blob/master/Contents/Database/sql-optimization) 2019.2.23
* [InnoDB 行锁的实现](https://github.com/vonzhou/Blog/blob/master/Contents/Database/innodb-row-lock) 2019.2.16

## Reading

* [何为整洁架构？](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/cleanarch/clean-arch.md) 2019.1.8
* [《非暴力沟通》读书笔记](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/nonviolent-communication.md)
* [2018阅读书单](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/2018-read-book.md)  2018.12.16
* [2017阅读书单](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/2017-read-book.md) 2018.1.3
* [2016阅读书单](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/2016-read-book.md) 2016.12.10
* [2015阅读书单](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/2015%E9%98%85%E8%AF%BB%E4%B9%A6%E5%8D%95.md)  2016.4.6



## Life

## Other 其他

* [历史文章列表](https://github.com/vonzhou/Blog/blob/master/Contents/Other/history-blogs.md)  2018.12.14








