---
title: "HBase 查询优化"
date: 2019-04-03
draft: false
categories: ["HBase"]
tags: ["HBase", "Java"]
---

## 场景

在[《HBase 实现分页查询》](http://vonzhou.com/2019/hbase-page/)中描述了一个按用户维度和时间区间查询HBase的场景，业务不断复杂后衍生出了另一个场景：需要查询一段时间段内，一个列符合特定条件的数据。

假设我们要查询的数据领域模型如下：

```java
class BigMsg {
    private Long id;
    private Long insertTime;
    private List<Long> a;
    private Long b;
    private String c;
}
```

问题抽象为：从HBase查询列b=b0的数据，其中b很稀疏。

```java
Long b0 = 123;
getDetailMsgs(b0);
```

## 行键设计与查询性能

HBase使用时最重要的莫过于Rowkey的设计，直接影响数据的存储和查询性能。

在我们的场景中，为了实现按照时间区间查询，rowkey包括用户ID和时间戳，可以使用过滤器，Scan的时候取我们需要的数据，在数据量很大的情况下，大量的KeyValue会送到过滤器筛选，必然很低效。


## 经验法则

* rowkey不宜过长
* 尽量将查询的维度或信息存储在rowkey中，因为rowkey筛选数据的效率最高

下面这张图来源于《HBase权威指南》，展示了KeyValue的各个方面对筛选数据性能的影响。

![从左到右查询性能逐渐降低](/images/hbase-query-optimize-1.png)

## 优化方案

回到我们的问题上来。

要查询一段时间内，列b=b0的数据，能想到有3种方法。

### 使用Filter

最直接的想法是Scan的时候设置列值过滤器，但是列b稀疏，所以在这样的效率很低。

### rowkey中包含

可以在设计rowkey的时候纳入列b的信息，这样方法存在以下缺陷：

* 会增加rowkey的存储开销
* 一开始设计rowkey的时候，并不能考虑到所有类似情况，所以灵活性不好

### 映射表

本人在实际中采用的是引入一个映射表的方法，映射表中存储了对应的列b和Msg HTable的rowkey之间的关联信息。

## 实现

### 映射信息存储

BigMsg信息的存储见《HBase 实现分页查询》，之后需要同时更新映射信息。

```java
public void saveMapInfo(BigMsg msg, String msgRowkey) {
    Long b = msg.getB();
    Long insertTime = msg.getInsertTime();
    // 将id作为rowkey的一部分，防止分布式环境下重复
    Long id = msg.getId();
    try {
        Table table = getTable();
 		Put p = new Put(getRowKey(b, insertTime, id));
        p.addColumn(Bytes.toBytes(COL_FAMILY), 			Bytes.toBytes(MSG_ID_COL), Bytes.toBytes(msgRowkey));
        table.put(put);
    } catch (Exception e) {
    }
}
```

### 查询

有了映射表，查询的时候就按时间范围先从映射表的时候Scan得到BigMsg HTable的rowkey，然后根据rowkey，使用批量Get从BigMsg HTable中查询得到最终的数据。

```java
public void getDetailMsgs(Long b) throws Exception {
    // 全量的
    long start = 0L;
    long end = System.currentTimeMillis();

    Filter filter = new PageFilter(100);

    byte[] lastRow = null;
    byte[] startRow = getRowKey(b, end, 0L);
    byte[] endRow = getRowKey(b, start, Long.MAX_VALUE);

	// 映射表
    Table table = getTable();
    while (true) {
        Scan scan = new Scan();
        scan.setFilter(filter);

        byte[] sr = null;
        if (lastRow != null) {
            sr = Bytes.add(lastRow, new byte[1]);
        } else {
            sr = startRow;
        }

        scan.setStartRow(sr);
        scan.setStopRow(endRow);
        ResultScanner scanner = table.getScanner(scan);
        Result result = null;
        int cnt = 0;
        List<String> msgRowkeys = new ArrayList<>();
        while ((result = scanner.next()) != null) {
            String rk = HBaseBytesUtil.getString(result.getValue(Bytes.toBytes(COL_FAMILY), Bytes.toBytes("id")));
            msgRowkeys.add(rk);
            cnt++;
            lastRow = result.getRow();
        }
        if (CollectionUtils.isNotEmpty(msgRowkeys)) {
            List<BigMsg> msgs = multiGet(msgRowkeys);
            // 处理 Msgs
            }
        }
        scanner.close();
        if (cnt == 0) {
            break;
        }
    }
}

public List<BigMsg> multiGet(List<String> msgRowkeys) throws Exception {
    List<BigMsg> res = new ArrayList<>();
    Table table = getMsgTable();

    List<Get> gets = new ArrayList<>();
    for (String r : msgRowkeys) {
        Get g = new Get(Bytes.toBytes(r));
        g.addFamily(Bytes.toBytes(COL_FAMILY));
        gets.add(g);
    }
    Result[] rs = table.get(gets);
    if (ArrayUtils.isNotEmpty(rs)) {
        for (Result r : rs) {
            res.add(getMsgFromResult(r));
        }
    }
    return res;
}
```

## 总结

* 充分挖掘应用场景，这样才能设计出良好的rowkey
* 使用映射表，其实也是变相的把需要检索的列移到了rowkey中，只不过是映射表的rowkey，这样可以不影响原始HTable的rowkey










