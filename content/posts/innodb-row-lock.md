---
title: "InnoDB 行锁的实现"
date: 2019-02-16
draft: false
categories: ["MySQL"]
tags: [ "MySQL", "InnoDB", "Lock"]
---


InnoDB 实现行锁（row lock）的3种算法：

* `Record Lock`：单行记录上锁
* `Gap Lock`：间隙锁，锁定一个范围，不包括记录本身
* `Next-key Lock`：等价于`Gap Lock` + `Record Lock`，即锁定一个范围同时锁定记录本身，为了解决Phantom Problem。

## 行加锁过程

InnoDB的行锁其实是索引记录锁，InnoDB存储引擎下每个表有一个主键（聚集索引），辅助索引中包含主键，根据查询使用的索引不同加锁也不同。

1. 通过主键加锁，仅对聚集索引记录进行加锁，`Record Lock`
2. 通过辅助索引进行加锁，需要先对辅助索引加锁 `Gap Lock`，再对聚集索引加锁 `Record Lock`
3. 当辅助索引是唯一索引的时候，`Next-key Lock`会降级为 `Record Lock`


## 实例

### 唯一索引行锁定


```sql
create table t (a int primary key);
insert into t values(1),(2),(5);
```


![唯一索引行锁定](/images/innodb-row-lock-1.jpg)

会话A会对a=5的行进行X锁定，由于a是主键且唯一，所以只会对这一行进行锁定，所以在会话B中插入a=4不会阻塞。

### 辅助索引行锁定

```sql
create table t2 (a int, b int, primary key(a), key(b));
insert into t2 values(1,1),(3,1),(5,3),(7,6),(10,8);
```

![辅助索引行锁定-记录锁](/images/innodb-row-lock-2.jpg)

会话A对a=5的聚簇索引行加了Record Lock，所以会话B会阻塞。

![辅助索引行锁定-间隙锁](/images/innodb-row-lock-3.jpg)

会话A不仅对a=5的聚簇索引行加了Record Lock，也会对辅助索引加 Next-Key Lock，锁定的范围是 (1,3],(3,6)。

所以在会话B中执行`insert into t2 values(13,3);`, `insert into t2 values(14,5);`也是同样的情况。

但是插入`b=0`, `b=1`, `b=5`, `b=6`时不会阻塞。

## 相关

[14.10.1 InnoDB Locking](https://dev.mysql.com/doc/refman/5.5/en/innodb-locking.html)









