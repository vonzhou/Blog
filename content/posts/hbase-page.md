---
title: "HBase 实现分页查询"
date: 2019-03-14
draft: false
categories: ["大数据"]
tags: ["HBase", "Java"]
---

## 序

按时间区间分页导出HBase中的数据。

## Rowkey的设计

在使用HBase时，Rowkey的设计很重要，取决于业务。

比如要把用户关联的数据存入HBase，后续根据时间查询，可以这样设计rowkey：

```
userId + (Long.MAX - timestamp) + uid 
```

这样能满足：

* 可以根据userId的特点预分区
* 时间戳逆转，可以保证最近的数据rowkey排序靠前
* 分布式环境下时间戳可能一样，所以追加一个UID，防止重复

示例代码：

```java
private String getRowKeyStr(String userId, long ts, long uid) {
    return String.format("%s%013d%019d", userId, Long.MAX_VALUE - ts, uid);
}
```


## 构造Table实例

需要自己保证Table的线程安全性。

```java
public Table getTable() throws Exception {
    Table table = tableThreadLocal.get();
    if (table == null) {
        table = getTableInternal();
        if (table != null) {
            tableThreadLocal.set(table);
        }
    }
    return table;
}

public Table getTableInternal() throws Exception {
    Configuration config = HBaseConfiguration.create();
    config.set(HConstants.ZOOKEEPER_QUORUM, hBaseConfig.getZkQuorum());
    config.set(HConstants.ZOOKEEPER_CLIENT_PORT, hBaseConfig.getZkClientPort());
    config.set(HConstants.ZOOKEEPER_ZNODE_PARENT, hBaseConfig.getZkZnodeParent());
    config.setInt("hbase.rpc.timeout", 20000);
    config.setInt("hbase.client.operation.timeout", 30000);
    config.setInt("hbase.client.scanner.timeout.period", 20000);
    config.setInt("hbase.client.pause", 50);
    config.setInt("hbase.client.retries.number", 15);
//        HBaseAdmin.checkHBaseAvailable(config);

    Connection connection = ConnectionFactory.createConnection(config);
    Table table = connection.getTable(TableName.valueOf(hBaseConfig.getTableName()));

    return table;
}
```

## 分页查询

这里要注意是Scan中的startRow，stopRow是左闭右开区间，所以为了避免下一页中包含上一页的最后一条数据， 下一页Scan的时候startRow追加了一个0字节。

```java
Filter filter = new PageFilter(15);

byte[] lastRow = null;
byte[] startRow = getRowKey(userId, end, 0L);
byte[] endRow = getRowKey(userId, start, Long.MAX_VALUE);

Table table = getTable();
if (table == null) {
    return;
}

int sum = 0;

while (true) {
    Scan scan = new Scan();
    scan.setFilter(filter);

    byte[] sr = null;
    if (lastRow != null) {
        sr = Bytes.add(lastRow, new byte[1]);// 重点1
    } else {
        sr = startRow;
    }
    scan.setStartRow(sr);
    scan.setStopRow(endRow);
    ResultScanner scanner = table.getScanner(scan);
    Result result = null;
    int cnt = 0;
    while ((result = scanner.next()) != null) {
        // 从Result中解析数据，进行处理
        cnt++;
        lastRow = result.getRow();
    }
    scanner.close();
    if (cnt == 0) {
        break;
    }
}
```

## Filter

上述只是用了PageFilter实现分页，如果需要根据列的各种条件进行查询，就需要用到FilterList，或者自己实现Filter。










