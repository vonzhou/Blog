[主页](http://vonzhou.com)  | [读书](https://github.com/vonzhou/readings)  | [知乎](https://www.zhihu.com/people/vonzhou) | [GitHub](https://github.com/vonzhou)
---

# MySQL Cheatsheet（MySQL常用知识备忘）

## 1. 数据类型


|  Type | Storage|
|---|---|
|TINYINT|1B|
|SMALLINT|2B|
|MEDIUMINT|3B|
|INT|4B|
|BIGINT|8B|
|  TINYTEXT |           255 (2^8−1) bytes|
|      TEXT |        65,535 (2^16−1) bytes = 64 KiB|
|MEDIUMTEXT |    16,777,215 (2^24−1) bytes = 16 MiB|
|  LONGTEXT | 4,294,967,295 (2^32−1) bytes =  4 GiB|



## 2. Commands 命令

### 删除表

```sql
drop table tableName;
```

### 新增表

```sql
CREATE TABLE `tableName` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '数据库主键',
  `name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '名称',
   PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='说明';
```

### 修改表结构

```
ALTER TABLE tableName ADD issue_type tinyint(4) DEFAULT 0 COMMENT 'comment abc';
alter table tableName drop nick_name;
```

### 取消安全更新模式

```
SET SQL_SAFE_UPDATES = 0;
```

### 修改某列的值等于另一列

```
update tableName set col1=col2 where col1 = '';
```

### unique key 唯一索引


建表时设置：

```sql
CREATE TABLE `tableName` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '数据库主键',
  `name` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '名称',
   PRIMARY KEY (`id`),
   unique key uk(`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='说明';
```


新增：

```
ALTER TABLE tableName ADD UNIQUE KEY `productId_uk` (`product_id`);
```

### 新增索引

```
ALTER TABLE `table` ADD INDEX `product_id` (`product_id`)
```

## 删除表中所有数据

```
delete from tableName;
```

### 导出

```sql
 mysqldump -uxxxxxx -pyyyyyyy--all-databases > /tmp/all.sql
```

### 导出建表语句

```sql
mysqldump -h localhost -u root -p --no-data --compact  <db_name>
```


### 删除外键

```sql
alter table footable drop foreign key fooconstraint
```


### 查看线程状态

```sql
show full processlist;
```


```sql

```






