[主页](https://github.com/vonzhou/Blog)  | [读书](https://github.com/vonzhou/Blog/blob/master/Contents/Reading/readings.md)  | [知乎](https://www.zhihu.com/people/vonzhou) 
---
# SQL优化方法总结


![](images/sql-optimization-mind.jpg)


## 1.查询分析

### 执行计划

### 服务器性能剖析

`pt-query-digest`工具



## 2. 数据类型优化

* 选用更小的，简单的类型
* 尽量避免NULL
* 无符号整数存储IP地址


## 3. 高效索引

### 索引对查询的影响

* 聚簇索引（主键索引）
* 前缀索引

### 谨防索引失效的场景

* 索引字段设计为not null
* 能用between and就不要用in
* where 子句中使用!=或<>操作符也会扫全表


## 4. 特定查询类型的优化



### 优化LIMIT分页（offset过大问题）

在offset很大的时候，查询的代价非常高，因为他会导致MySQL扫描大量不需要的行然后抛弃掉，可以使用书签记录上次取数据的位置，避免使用offset。

```sql
select *from large_table where id < 18880 order by id desc limit 10;
```


### 优化关联查询

* 确保ON或者USING子句中的列上有索引。只需要在关联顺序中第二个表的相应列上创建索引。
* 确保任何的GROUP BY 和 ORDER BY中的表达式只涉及一个表中的列，这样才有可能使用索引来优化。


## 4. 应用层优化

### 是否请求了需要的数据

* 查询了大量不需要的列
* 总是查询全部的列

### 应用层缓存












