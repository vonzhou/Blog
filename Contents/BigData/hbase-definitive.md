[主页](http://vonzhou.com)  | [读书](https://github.com/vonzhou/readings)  | [知乎](https://www.zhihu.com/people/vonzhou) | [GitHub](https://github.com/vonzhou)
---
# 《HBase权威指南》读书笔记
---

我是在阅读《HBase不睡觉书》之后阅读的该书，所以没有通读。

## 思维导图

![](hbase-definitive-xmind.png)

## 笔记

在一个上规模的系统中，单一的DB已经无法满足需求，一般会引入多种数据系统，应对不同的场景。

阅读时可以先通过简介，架构章节认识HBase，理解了其底层原理才能更好的使用，遇到问题不会盲目。接下来需要自己把HBase平台搭建起来，也需要一番折腾，也能体会各种组件的关系（HBase，ZK，Hadoop），最后就可以使用hbase shell或者Java API使用HBase。


### 架构

BigTable底层的存储架构是 LSM， 和B+ tree对比， 区别是如何利用磁盘。

读写流程：

![](hbase-read-write-flow.png)

合并：在Region server中随着数据的写入，Memstore会刷到磁盘上，生成很多文件，如果这些文件的数目达到阈值，就会执行minor合并，生成更大的文件。还有一种执行不会那么频繁的major合并，会把所有文件合并成一个大文件，当然如果这个大文件超过阈值则会触发一次Region split。

Region拆分：当一个Region里的存储文件达到配置的阈值（`hbase.hregion.max.filesize`）时会一分为二，在父region的`splits`目录下进行，然后会更新`.META.`表的状态和索引信息。

WAL：预写日志，类似于MySQL中的binlog，是为了保障RegionServer crash后数据不丢失的（前提是Hadoop是可靠的）。

### 使用

基本的API使用起来。

根据业务场景设计rowkey，长度不要太长，尽量分散。



## 相关阅读

《Design Data-Intensive Applications》关于LSM，列式存储的章节。





> 读于2018.12.20 杭州